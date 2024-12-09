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
load_dotenv()




def fetch_data(token):
    url = "https://open-api.openocean.finance/v4/eth/tokenList"
    headers = {"accept": "*/*"}

    # Make the request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the response JSON
        data = response.json().get("data", [])
        
        # Extract the required fields
        filtered_data = [
            {
                "name": token.get("name"),
                "address": token.get("address"),
                "symbol": token.get("symbol"),
                "chain": token.get("chain"),
            }
            for token in data
        ]
        
        print(filtered_data)  # Print or process the filtered data
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

    prompt= f''' 
        You are going to fetch the address and symbol of a token from the given list.

        Token: {token}

        list: {filtered_data}

give it in a json format

output format- 

    symbol: "symbol"// the symbol of the token
    addrerss: "address"// the address of the token

'''
    response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
 response_format={ "type": "json_object" }
)

# Print the assistant's reply
    return(response.choices[0].message.content)

def fetch_balance(prompt):
    url = "https://open-api.openocean.finance/v4/eth/tokenList"
    headers = {"accept": "*/*"}

    # Make the request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the response JSON
        data = response.json().get("data", [])
        
        # Extract the required fields
        filtered_data = [
            {
                "name": token.get("name"),
                "address": token.get("address"),
                "symbol": token.get("symbol"),
                "chain": token.get("chain"),
            }
            for token in data
        ]
        
        print("hi",filtered_data)  # Print or process the filtered data
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

    prompt= f''' 

            You should form an output like this:
json :
  "type": "balance",
  "data": 
    "address": "0x1234567890123456789012345678901234567890",
    "chain": ["137"], // can be null
    "token_address": ["0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"], // can be null
    "count": 10 // can be null eg: get top 10 balance
  ,
  "msg": "Here is your token balances list"

        based on the prompt : {prompt}

            There are 2 cases:
            1. If it's Get balance of a specific chain, or tokens make sure that the address should be a string and chain and tokens should be a list always. If count is not provided, it is always None.
            2. If it's Get all my balance, make sure that the chain and token_address should be empty list always. If count is not provided, it is always None.
 
            Don't forget to provide the  address, token_address,chain, and count in the parameters.
            NOTE: when the count is not in the user prompt, it is always None.
            Don't miss count parameter. Always provide it.

        You are going to fetch the address  of a token from the given list for the tokens present in the prompt for the token_address. 
        Look for the tokens names in the prompt and return the address of the token.
        Don't care about any other things in the present.
        If there is no tokens mentioned or present in the prompt. just return an empty list for the token_address.

        
        Don't take much time to do this task. Just do it quickly.

        list: {filtered_data}

give it in a json format

output format-
"type": "balance",
  "data": 
    "address": "0x1234567890123456789012345678901234567890",
    "chain": ["137"], // can be null
    "token_address": ["0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"], // can be null
    "count":  // Null if not present in the prompt
  ,
  "msg": "Here is your token balances list"


'''
    response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
 response_format={ "type": "json_object" }
)

# Print the assistant's reply
    return(response.choices[0].message.content)

def get_balance(prompt ):
    
  token_address = json.loads(fetch_balance(prompt))
  return token_address


import openai

def fetch_nft(prompt,address,chain):



    url = "https://buddy-dev.buildverse.app/api/nfts"


    params = {
  
        "address": address
    }
    if chain is not None:
        params["chainId"] = chain

    # Request body
    data = {
        "email": "dennis@dappgenie.io",
        "password": "$2a$10$MYHZRD1vWeMvPpUtTtpfj.3o9pP0OLtbiZYP8scgvBWJt0wSAYon6"
    }

    # Making the GET request
    response = requests.get(url, params=params, json=data)

    # Printing the response
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Failed with status code:", response.status_code)
        print("Response:", response.text)


    prompt= f''' 

            You should form an output like this:
json :

  "type": "nft_balance",
  "data": 
    "address": "0x1234567890123456789012345678901234567890",
    "chain": ["137"], // can be null
    "nftAddress": ["0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"], // can be null
    "count": // can be null eg:
  
  "msg": "Here is your NFTs list"


        based on the prompt : {prompt}

            There are 2 cases:
            1. If it's Get Nft of a specific chain, or nft id make sure that the address should be a string and chain and nftAddress should be a list always. If count is not provided, it is always None.
            2. If it's Get all my nfts or all my nft balance, make sure that the chain and nftAddress should be empty list always. If count is not provided, it is always None.
            if it's Get Nft of a nft id make sure that the chain is not None and pass the chain from the ctx.
            The nft address for a nft id is the contractId of the nft.
            the chain should be only list of chainIds or empty list. It should not have chain names
            .
            Don't forget to provide the  address, NftAddress,chain, and count in the parameters.
            NOTE: when the count is not in the user prompt, it is always None.
            Don't miss count parameter. Always provide it.

        You are going to fetch the contractId  of a nft from the given list for the nfts present in the prompt for the NftAddress. 
        Look for the nft ids in the prompt and compare it with the Nfts list and and return the contractId of the nft as NftAddress.
        Don't care about any other things in the present.
        Do not use any other information from the Nfts list other than the contractId.
        If there is no nfts mentioned or present in the prompt. just return an empty list for the nftAddress.

        NftAdress is an empty list if there are no nfts present in the prompt.
        Don't take much time to do this task. Just do it quickly.

        Nfts list: {response.json()}

give it in a json format

output format-

  "type": "nft_balance",
  "data": 
    "address": "",
    "chain": [], // can be null or list of chainids (should not have chain names)
    "nftAddress": [], // can be null
    "count": // can be null eg:
  
  "msg": "Here is your NFTs list"


'''
    response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
 response_format={ "type": "json_object" }
)

# Print the assistant's reply
    return(response.choices[0].message.content)

def get_nft_balance(prompt , address, chain = None):
    print(chain)
    nft = json.loads(fetch_nft(prompt,address,chain))
    return nft


def send_nft_to_address(nftId, chain, toAddress,nftAddress):
    return {
  "type": "send_nft",
  "data": {
    "address": toAddress,
    "chain": chain,
    "nftAddress": nftAddress,
    "nftId": nftId,
    "isContact": True
  },
  "msg": "Sure! The amount has been added and is ready for sending. Please review & click the 'Send' button to complete the transaction."
}

chain_map = {
    "Ethereum": {"chainId": 1, "symbol": "eth", "dbank": "eth"},
    "Optimism": {"chainId": 10, "symbol": "op", "dbank": "op"},
    "Arbitrum": {"chainId": 42161, "symbol": "arb", "dbank": "arb"},
    "Polygon": {"chainId": 137, "symbol": "matic", "dbank": "matic"},
    "Base": {"chainId": 8453, "symbol": "base", "dbank": "base"},
    "Celo": {"chainId": 42220, "symbol": "celo", "dbank": "celo"},
    "Blast": {"chainId": 81457, "symbol": "blast", "dbank": "blast"},
    "Avalanche": {"chainId": 43114, "symbol": "avax", "dbank": "avax"},
    "Fantom": {"chainId": 250, "symbol": "ftm", "dbank": "ftm"},  # Added Fantom
}



def send_eth_to_address(address,chain,amount):
    return {
  "type": "send_native",
  "data": {
    "address": address,
    "chain": chain,
    "amount": amount,
    "isContact": True
  },
  "msg": "Sure! The amount has been added and is ready for sending. Please review & click the 'Send' button to complete the transaction."
  
  }

def send_token_to_address(address,chain,amount):
    
  chainid_to_chain = {
    1: "eth",
    10: "op",
    42161: "arb",
    137: "matic",
    8453: "base",
    42220: "celo",
    81457: "blast",
    43114: "avax",
    250: "ftm"
}

  token_address = json.loads(fetch_data(chainid_to_chain[int(chain)]))["address"]
  return {
  "type": "send_token",
  "data": {
    "address": address,
    "chain": chain,
    "amount": amount,
    "tokenAddress": token_address,
    "isContact": True

  }}

def switch_network(chain_name):
    return {
  "type": "switch_network",
  "data": {
    "chain": chain_map[chain_name]["chainId"],
  },
  "msg": f"Sure! The network has been initiated to switch to {chain_name}. Please review & confirm in your wallet."
    }

def bridge_token(amount,ctx_chain_id, chain_name, token):
    symbol = json.loads(fetch_data(token))["symbol"]
    return{
    "type": "bridge_token",
    "data": {
    "fromChainId": ctx_chain_id,
    "toChainId": chain_map[chain_name]["chainId"],
    "fromSymbol": symbol,
    "toSymbol": symbol,
    "amount": amount,
    },
    "msg": "Sure! The amounts and token addresses have been added and are ready for bridging. Please review & click the 'Bridge' button to complete the transaction."
    }

def swap_token(amount, chain, fromToken, toToken):

    intoken_address = json.loads(fetch_data(fromToken))["address"]
    outtoken_address = json.loads(fetch_data(toToken))["address"]

    return {
  "type": "swap_token",
  "data": {
    "chain": chain,
    "inTokenAddress ": intoken_address,
    "outTokenAddress ": outtoken_address,
    "amount": amount,
  },
  "msg": "Sure! The amounts and token addresses have been added and are ready for swapping. Please review & click the 'Swap' button to complete the transaction."
}