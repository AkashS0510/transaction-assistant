from fastapi import FastAPI
from typing import List, Dict, Union , Optional
from dotenv import load_dotenv
from typing import List, Dict, Union , Optional
import requests
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import openai
from enum import Enum

from dotenv import load_dotenv
from tools import *
from models import *
load_dotenv()






from openai import OpenAI
client = OpenAI()


assistant = client.beta.assistants.create(
    name="crypto transactions and wallet assistant",
    instructions='''You are an expert that helps with crypto transactions and wallet queries. You are capable of :

  1. Get user balance
  2. Get user NFTs
  3. Send ETH to address
  4. Send token to address
  5. Send NFT to address
  6. Switch network
  7. Swap token
  8. Bridge token

You can use the available tools to perform the above tasks.

You should not do any tasks other than the above mentioned tasks.

Do not take much time to do the tasks. Do it quickly.  

"
  
  ''',
    tools=[{
        "type": "function",
        "function": {
            "name": "send_eth_to_address_tool",
            "description": "Send ETH to an address",
            "parameters": SendEthRequest.model_json_schema()
        }
    },
    {
    "type": "function",
        "function": {
            "name": "send_token_to_address_tool",
            "description": "Send Token to an address",
            "parameters": SendTokenRequest.model_json_schema()
        } },

        {
    "type": "function",
        "function": {
            "name": "switch_network_tool",
            "description": "Switch Network. Only Ethereum, Optimism, Arbitrum, Polygon, Base, Celo, Blast, Avalanche, Fantom are supported. ",
            "parameters": SwitchNetworkRequest.model_json_schema()
        }},
    {
    "type": "function",
        "function": {
            "name": "bridge_token_tool",
            "description": "Bridge Token. Only Ethereum, Optimism, Arbitrum, Polygon, Base, Celo, Blast, Avalanche, Fantom are supported. ",
            "parameters": BridgeTokenRequest.model_json_schema()
        }},
    {
    "type": "function",
        "function": {
            "name": "swap_token_tool",
            "description": "Swap Token. ",
            "parameters": SwapTokenRequest.model_json_schema()
        }},

    {
    "type": "function",
        "function": {
            "name": "get_balance_tool",
            "description": """Get the balance. 
                    pass the prompt with the ctx as it is without any changes. Call this tool only once even if there is mutiple tokens pass everything in a single prompt. Pass the whole prompt in one go.
            """,
            "parameters": GetBalanceRequest.model_json_schema()
        }},

        {

    "type": "function",
        "function": {
            "name": "get_nft_balance_tool",
            "description": """Get the NFT balance. 
                    pass the prompt with the ctx as it is without any changes. Call this tool only once even if there is mutiple nfts pass everything in a single prompt. Pass the whole prompt in one go.
                    If it's Get all my nfts or all my nft balance, make sure that the chain is None.
                    if it's Get Nft of a  nft id make sure that the chain is not None and pass the chain from the ctx.

                    NOTE: Do not make mutiple calls to this tool. Call it only once using the whole prompt.
            """,
            "parameters": GetNftBalanceRequest.model_json_schema()
        }},

        {

    "type": "function",
        "function": {
            "name": "send_nft_to_address_tool",
            "description": "Send NFT to an address.  Use this tool to send NFT to an address. pass the nftId, chain, toAddress, nftAddress from the prompt. example prompt text:  Send nft 27 of 0x1234567890123456789012345678901234567890 to 0x1234567890123456789012345678901234567890 ",
            "parameters": SendNftRequest.model_json_schema()


        }}


    ],

    
    model="gpt-4o-mini",
)

def handle_message(message_text, thread_id):
    message = client.beta.threads.messages.create(
  thread_id=thread_id,
  role="user",
  content=message_text
)
    
    messagerun = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant.id
)
    
    return messagerun

def handle_tool_execution(tool_name, parsed_arguments):
    """Executes the tool based on its name and returns the result."""
    if tool_name == "send_eth_to_address_tool":
        address = parsed_arguments["address"]
        chain = parsed_arguments["chain"]
        amount = parsed_arguments["amount"]
        result = send_eth_to_address(address,chain,amount)
        return result
    elif tool_name == "send_token_to_address_tool":
        address = parsed_arguments["address"]
        chain = parsed_arguments["chain"]
        amount = parsed_arguments["amount"]
        result = send_token_to_address(address,chain,amount)
        return result
    elif tool_name == "switch_network_tool":
        chain = parsed_arguments["chainName"]
        result = switch_network(chain)
        return result
    elif tool_name == "bridge_token_tool":
        amount = parsed_arguments["amount"]
        chain = parsed_arguments["ctx_chain_id"]
        chain_name = parsed_arguments["chain_name"]
        token = parsed_arguments["token"]
        result = bridge_token(amount,chain, chain_name, token)
        return result
    elif tool_name == "swap_token_tool":
        amount = parsed_arguments["amount"]
        chain = parsed_arguments["chain"]
        fromToken = parsed_arguments["fromToken"]
        toToken = parsed_arguments["toToken"]
        result = swap_token(amount, chain, fromToken, toToken)
        return result
    elif tool_name == "get_balance_tool":
        prompt = parsed_arguments["prompt"]
        print(prompt)
        result = get_balance(prompt)
        return result
    elif tool_name == "get_nft_balance_tool":
        prompt = parsed_arguments["prompt"]
        address = parsed_arguments["address"]
        chain = parsed_arguments["chain"]
        result = get_nft_balance(prompt,address,chain)
        return result
    elif tool_name == "send_nft_to_address_tool":
        nftId = parsed_arguments["nftId"]
        chain = parsed_arguments["chain"]
        toAddress = parsed_arguments["toAddress"]
        nftAddress = parsed_arguments["nftAddress"]
        result = send_nft_to_address(nftId, chain, toAddress,nftAddress)
        return result
    
    else:
        raise ValueError(f"Tool '{tool_name}' is not recognized.")
    


def submit_tool_outputs(thread_id, run_id, tool_outputs):
    """Submits the tool outputs back to the assistant and polls the result."""
    # Submit the tool outputs and poll for further updates
    client.beta.threads.runs.submit_tool_outputs_and_poll(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )


def handle_run_response(thread_id, run):
    """Handles the response of a run based on its status."""
    if run.status == 'completed':
        # Fetch the latest message in the thread if the run is completed
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        latest_message = messages.data[0]
        
        # Access the content of the latest message
        latest_message_content = latest_message.content[-1].text.value if latest_message.content else "No content available"
        return latest_message_content

    elif run.status == 'requires_action':
        required_action = run.required_action

        # Check if the required action contains tool calls
        if required_action and hasattr(required_action, "submit_tool_outputs"):
            tool_calls = required_action.submit_tool_outputs.tool_calls
            
            if tool_calls:
                tool_outputs = []
                # Process each tool call in the list of tool calls
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_arguments = tool_call.function.arguments
                    
                    # Parse the JSON arguments into a Python dictionary
                    parsed_arguments = json.loads(tool_arguments)
                    
                    try:
                        # Execute the tool and get the result
                        result = handle_tool_execution(tool_name, parsed_arguments)

                        # Convert Pydantic model result to a dictionary if needed
                        if isinstance(result, BaseModel):
                            result = result.model_dump()

                        # Append the tool call output to the list
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)  # Convert the result to a JSON string
                        })
                    
                    except ValueError as e:
                        print(f"Error during tool execution: {e}")
                        return {"Error": str(e)}

                # Submit all tool outputs together
                submit_tool_outputs(thread_id, run.id, tool_outputs)
                return tool_outputs
            else:
                print("No tool calls found in the required action.")
        else:
            print("No tool invocation required or recognized action.")
    else:
        print(f"Unhandled run status: {run.status}")



def chat_with_assistant(prompt, new, id_thread= None):
    if new == True:
        thread = client.beta.threads.create()
        id = thread.id
    else:
        id = id_thread
    # print(id)
    messagerun=handle_message(prompt, thread_id=id)
    # print(messagerun.id)
    if messagerun.status == 'requires_action':
        response= handle_run_response(run= messagerun,thread_id=id)
        response= json.loads(response[0]["output"])
        runInfo = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=messagerun.id)
        if runInfo.completed_at ==None:
            client.beta.threads.runs.cancel(messagerun.id,thread_id=id)

    else:
        response= handle_run_response(run= messagerun,thread_id=id)

    return {"id": id, "response" : response}