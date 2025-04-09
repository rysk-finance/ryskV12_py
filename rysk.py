from dataclasses import dataclass
from enum import Enum
import subprocess
import sys
from typing import Any, Callable, List

from models import Quote, Transfer


class Env(Enum):
    LOCAL = 0
    TESTNET = 1
    MAINNET = 2


@dataclass(frozen=True)
class EnvConfig:
    base_url: str


ENV_CONFIGS = {
    Env.LOCAL: EnvConfig("ws://localhost:8000/"),
    Env.TESTNET: EnvConfig("wss://rip-testnet.rysk.finance/"),
}


class Rysk:
    _env: Env
    _cli_path: str
    _private_key: str

    def __init__(
        self,
        env: Env,
        private_key: str,
        v12_cli_path: str = "./ryskV12",
    ):
        self._env = env
        self._cli_path = v12_cli_path
        self._private_key = private_key

    def _url(self, uri: str) -> str:
        return f"{ENV_CONFIGS.get(self._env).base_url}{uri}"

    def execute(
        self,
        args: List[str] = [],
        on_message: Callable[[str], Any] = print,
        on_error: Callable[[str], Any] = lambda err: print(err, file=sys.stderr),
        on_close: Callable[[int], Any] = print,
    ) -> None:
        process = subprocess.Popen(
            [self._cli_path, *args],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if process.stdout:
            for line in process.stdout:
                on_message(line.strip())

        if process.stderr:
            for line in process.stderr:
                on_message(line.strip())

        returncode = process.wait()
        on_close(returncode)
        if returncode != 0:
            on_error(
                subprocess.CalledProcessError(returncode, [self._cli_path, *args])
            )

    def connect_args(self, channel_id: str, uri: str) -> List[str]:
        return ["connect", "--channel_id", channel_id, "--url", self._url(uri)]

    def approve_args(self, chain_id: int, amount: str, rpc_url: str) -> List[str]:
        return [
            "approve",
            "--chain_id",
            str(chain_id),
            "--amount",
            amount,
            "--rpc_url",
            rpc_url,
            "--private_key",
            self._private_key,
        ]

    def balances_args(self, channel_id: str, account: str) -> List[str]:
        return ["balances", "--channel_id", channel_id, "--account", account]

    def transfer_args(self, channel_id: str, transfer: Transfer) -> List[str]:
        return [
            "transfer",
            "--channel_id",
            channel_id,
            "--chain_id",
            str(transfer.chain_id),
            "--asset",
            transfer.asset,
            "--amount",
            transfer.amout,
            "--is_deposit" if transfer.is_deposit else "",
            "--nonce",
            transfer.nonce,
            "--private_key",
            self._private_key,
        ]

    def positions_args(self, channel_id: str, account: str) -> List[str]:
        return ["positions", "--channel_id", channel_id, "--account", account]

    def quote_args(self, channel_id: str, rfq_id: str, quote: Quote) -> List[str]:
        return [
            "quote",
            "--channel_id",
            channel_id,
            "--rfq_id",
            rfq_id,
            "--asset_address",
            quote.assetAddress,
            "--chain_id",
            str(quote.chainId),
            "--expiry",
            str(quote.expiry),
            "--is_put" if quote.isPut else "",
            "--is_taker_buy" if quote.isTakerBuy else "",
            "--maker",
            quote.maker,
            "--nonce",
            quote.nonce,
            "--price",
            quote.price,
            quote.quantity,
            quote.strike,
            str(quote.validUntil),
            "--private_key",
            self._private_key,
        ]
