import asyncio
from dataclasses import dataclass
from enum import Enum
from os import path
from subprocess import PIPE, Popen
from typing import List

from .models import Quote, Transfer


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

    def _url(self, uri: str):
        return f"{ENV_CONFIGS.get(self._env).base_url}{uri}"
    
    def setup(self):
        script_path = path.join(path.dirname(path.abspath(__file__)), "scripts/fetch_latest_release.sh")
        Popen(
            ["chmod", "+x", script_path],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )
        Popen(
            [
                script_path
            ],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )
        Popen(
            ["chmod", "+x", "ryskV12"],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )

    def execute(self, args: List[str] = []):
        return Popen(
            [self._cli_path, *args],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )

    async def execute_async(self, args: List[str] = [], callback = print):
        process = await asyncio.create_subprocess_exec(
            self._cli_path,
            *args,
            stdout=PIPE,
            stderr=PIPE,
            text=False,
        )
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            callback(line)  
        return await process.wait()

    def connect_args(self, channel_id: str, uri: str):
        return ["connect", "--channel_id", channel_id, "--url", self._url(uri)]

    def disconnect_args(self, channel_id: str):
        return ["disconnect", "--channel_id", channel_id]

    def approve_args(self, chain_id: int, amount: str, rpc_url: str):
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

    def balances_args(self, channel_id: str, account: str):
        return ["balances", "--channel_id", channel_id, "--account", account]

    def transfer_args(self, channel_id: str, transfer: Transfer):
        base = [
            "transfer",
            "--channel_id",
            channel_id,
            "--chain_id",
            str(transfer.chain_id),
            "--asset",
            transfer.asset,
            "--amount",
            transfer.amout,
            "--nonce",
            transfer.nonce,
            "--private_key",
            self._private_key,
        ]
        if transfer.is_deposit:
            base.append("--is_deposit")
        return base

    def positions_args(self, channel_id: str, account: str):
        return ["positions", "--channel_id", channel_id, "--account", account]

    def quote_args(self, channel_id: str, rfq_id: str, quote: Quote):
        base = [
            "quote",
            "--channel_id",
            channel_id,
            "--rfq_id",
            rfq_id,
            "--asset",
            quote.assetAddress,
            "--chain_id",
            str(quote.chainId),
            "--expiry",
            f"{quote.expiry}",
            "--maker",
            quote.maker,
            "--nonce",
            quote.nonce,
            "--price",
            quote.price,
            "--quantity",
            quote.quantity,
            "--strike",
            quote.strike,
            "--valid_until",
            str(quote.validUntil),
            "--private_key",
            self._private_key,
        ]
        if quote.isPut:
            base.append("--is_put")
        if quote.isTakerBuy:
            base.append("--is_taker_buy")
        return base

