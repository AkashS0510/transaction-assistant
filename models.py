from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
from enum import Enum


class SendEthRequest(BaseModel):
    address: str = Field(description="The address to send to")
    chain: str = Field(description="The current chain ID in the ctx. example  ctx: {chain: 137 }. It is a number")
    amount: str

class SendTokenRequest(BaseModel):
    address: str = Field(description="The address to send to")
    chain: str
    amount: str = Field(description="The amount to send. have only the digits")


class GetBalanceRequest(BaseModel):
    prompt: str = Field(description="The full prompt along with the ctx.")

class ChainName(str, Enum):
    ethereum = "Ethereum"
    optimism = "Optimism"
    arbitrum = "Arbitrum"
    polygon = "Polygon"
    base = "Base"
    celo = "Celo"
    blast = "Blast"
    avalanche = "Avalanche"
    fantom = "Fantom"

    
class SwitchNetworkRequest(BaseModel):
    chainName: ChainName


class SwapTokenRequest(BaseModel):
    amount: str
    chain: str  = Field(description="The chain id of the token in the ctx. example  ctx: {chain: }")
    fromToken: str
    toToken: str

class BridgeTokenRequest(BaseModel):
    amount: str
    ctx_chain_id: str = Field(description="The chain id of the token in the ctx. example  ctx: {chain: }")
    chain_name: ChainName
    token: str


class GetNftBalanceRequest(BaseModel):
    prompt: str = Field(description="The full prompt along with the ctx.")
    address: str = Field(description="The address in the ctx")
    chain: str = Field(description="The chain id ")

class SendNftRequest(BaseModel):
    nftId: str  = Field(description="The nft id")
    chain: str = Field(description="The chain id")
    toAddress: str = Field(description="The address to send to")
    nftAddress: str = Field(description="The address of the nft")
