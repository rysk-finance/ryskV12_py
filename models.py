from dataclasses import dataclass
import json
from typing import Any, Callable, Dict, List, Literal, Union


@dataclass(frozen=True)
class Request:
    asset: str
    assetName: str
    chainId: int
    expiry: int
    isPut: bool
    quantity: str
    strike: str
    taker: str

    @staticmethod
    def from_json(data: str) -> "Request":
        j = json.loads(data)
        return Request(
            asset=j.get("asset"),
            assetName=j.get("assetName"),
            chainId=j.get("chainId"),
            expiry=j.get("expiry"),
            isPut=j.get("isPut"),
            quantity=j.get("quantity"),
            strike=j.get("strike"),
            taker=j.get("taker"),
        )


@dataclass(frozen=True)
class Quote:
    assetAddress: str
    chainId: int
    expiry: int
    isPut: bool
    isTakerBuy: bool
    maker: str
    nonce: str
    price: str
    quantity: str
    strike: str
    validUntil: int

    @staticmethod
    def from_json(data: str) -> "Quote":
        j = json.loads(data)
        return Quote(
            assetAddress=j.get("assetAddress"),
            chainId=j.get("chainId"),
            expiry=j.get("expiry"),
            isPut=j.get("isPut"),
            isTakerBuy=j.get("isTakerBuy"),
            maker=j.get("maker"),
            nonce=j.get("nonce"),
            price=j.get("price"),
            quantity=j.get("quantity"),
            strike=j.get("strike"),
            validUntil=j.get("validUntil"),
        )


@dataclass(frozen=True)
class QuoteNotification:
    rfqId: str
    assetAddress: str
    chainId: int
    newBest: str
    yours: str

    @staticmethod
    def from_json(data: str) -> "QuoteNotification":
        j = json.loads(data)
        return QuoteNotification(
            rfqId=j.get("rfqId"),
            assetAddress=j.get("assetAddress"),
            chainId=j.get("chainId"),
            newBest=j.get("newBest"),
            yours=j.get("yours"),
        )


@dataclass(frozen=True)
class Transfer:
    amout: str
    asset: str
    chain_id: int
    is_deposit: bool
    nonce: str

    @staticmethod
    def from_json(data: str) -> "Transfer":
        j = json.loads(data)
        return Transfer(
            amout=j.get("amout"),
            asset=j.get("asset"),
            chain_id=j.get("chain_id"),
            is_deposit=j.get("is_deposit"),
            nonce=j.get("nonce"),
        )


@dataclass(frozen=True)
class JSONRPCResponse:
    jsonrpc: Literal["2.0"]
    id: str
    method: str
    params: Union[Dict[str, Any], List[Any], str, None]

    @staticmethod
    def from_json(data: str) -> "JSONRPCResponse":
        j = json.loads(data)
        return JSONRPCResponse(
            jsonrpc=j.get("jsonrpc"),
            id=j.get("id"),
            method=j.get("method"),
            params=j.get("params"),
        )


JSONResponseHandler = Callable[[JSONRPCResponse], None]
