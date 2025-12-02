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
    usd: str
    collateralAsset: str

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
            usd=j.get("usd"),
            collateralAsset=j.get("collateralAsset")
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
    usd: str
    collateralAsset: str


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
    user: str
    amout: str
    asset: str
    chain_id: int
    is_deposit: bool
    nonce: str


@dataclass(frozen=True)
class JSONRPCResponse:
    jsonrpc: Literal["2.0"]
    id: str
    result: Union[Dict[str, Any], List[Any], str, None]

    @staticmethod
    def from_json(data: str) -> "JSONRPCResponse":
        j = json.loads(data)
        return JSONRPCResponse(
            jsonrpc=j.get("jsonrpc"),
            id=j.get("id"),
            result=j.get("result"),
        )


JSONResponseHandler = Callable[[JSONRPCResponse], None]


from typing import Any, Dict, List, Union


def is_request(obj: Any) -> bool:
    """Type predicate for Request."""
    return (
        isinstance(obj, dict)
        and obj is not None
        and isinstance(obj.get("asset"), str)
        and isinstance(obj.get("assetName"), str)
        and isinstance(obj.get("chainId"), int)
        and isinstance(obj.get("expiry"), int)
        and isinstance(obj.get("isPut"), bool)
        and isinstance(obj.get("quantity"), str)
        and isinstance(obj.get("strike"), str)
        and isinstance(obj.get("taker"), str)
        and isinstance(obj.get("usd"), str)
        and isinstance(obj.get("collateralAsset"), str)
    )


def is_quote(obj: Any) -> bool:
    """Type predicate for Quote."""
    return (
        isinstance(obj, dict)
        and obj is not None
        and isinstance(obj.get("assetAddress"), str)
        and isinstance(obj.get("chainId"), int)
        and isinstance(obj.get("expiry"), int)
        and isinstance(obj.get("isPut"), bool)
        and isinstance(obj.get("isTakerBuy"), bool)
        and isinstance(obj.get("maker"), str)
        and isinstance(obj.get("nonce"), str)
        and isinstance(obj.get("price"), str)
        and isinstance(obj.get("quantity"), str)
        and isinstance(obj.get("signature"), str)
        and isinstance(obj.get("strike"), str)
        and isinstance(obj.get("validUntil"), int)
        and isinstance(obj.get("usd"), str)
        and isinstance(obj.get("collateralAsset"), str)
    )


def is_transfer(obj: Any) -> bool:
    """Type predicate for Transfer."""
    return (
        isinstance(obj, dict)
        and obj is not None
        and isinstance(obj.get("user"), str)
        and isinstance(obj.get("amout"), str)
        and isinstance(obj.get("asset"), str)
        and isinstance(obj.get("chain_id"), int)
        and isinstance(obj.get("isDeposit"), bool)
        and isinstance(obj.get("nonce"), str)
    )


def is_json_rpc_response(obj: Any) -> bool:
    """Type predicate for JSONRPCResponse."""
    return (
        isinstance(obj, dict)
        and obj is not None
        and isinstance(obj.get("jsonrpc"), str)
        and isinstance(obj.get("id"), str)
        and (
            isinstance(obj.get("result"), dict)
            or isinstance(obj.get("result"), list)
            or isinstance(obj.get("result"), str)
        )
    )


def is_quote_notification(obj: Any) -> bool:
    """Type predicate for QuoteNotification."""
    return (
        isinstance(obj, dict)
        and obj is not None
        and isinstance(obj.get("rfqId"), str)
        and isinstance(obj.get("assetAddress"), str)
        and isinstance(obj.get("chainId"), int)
        and isinstance(obj.get("newBest"), str)
        and isinstance(obj.get("yours"), str)
    )
