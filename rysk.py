from dataclasses import dataclass
from enum import Enum
import json
import subprocess
import shlex
import sys
import time

from models import JSONRPCResponse, JSONResponseHandler, Quote, Transfer

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

    def connect(self, channel_id: str, uri: str, handler: JSONResponseHandler):
        """
        Instantiate a new websocket connection with a given id.
        """
        try:
            command = shlex.split(
                f"{self._cli_path} connect --channel_id {channel_id} --url {self._url(uri)}"
            )
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if process.stdout:
                while True:
                    line = process.stdout.readline().strip()
                    if not line:
                        if process.poll() is not None:
                            break
                        time.sleep(0.1)
                        continue
                    try:
                        res: JSONRPCResponse = json.loads(line)
                        handler(res)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}, line: {line}", file=sys.stderr)

            if process.stderr:
                for line in process.stderr:
                    print(f"CLI error: {line.strip()}", file=sys.stderr)

            process.wait()
            if process.returncode != 0:
                print(
                    f"CLI process exited with code {process.returncode}",
                    file=sys.stderr,
                )

        except Exception as e:
            print(f"Exception raised {e}", file=sys.stderr)

    def approve(self, channel_id: str, chain_id: int, amount: str):
        subprocess.run(
            [
                self._cli_path,
                "approve",
                "--channel_id",
                channel_id,
                "--chain_id",
                str(chain_id),
                "--amount",
                amount,
                "--private_key",
                self._private_key,
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )

    def balances(self, channel_id: str, account: str):
        subprocess.run(
            [
                self._cli_path,
                "balances",
                "--channel_id",
                channel_id,
                "--account",
                account,
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )

    def transfer(self, channel_id: str, transfer: Transfer):
        """
        Send a transfer request through the given channel_id.
        The response will be readable through the channel output.
        """
        subprocess.run(
            [
                self._cli_path,
                "transfer",
                "--channel_id",
                channel_id,
                "--chain_id",
                str(transfer.chain_id),
                "--asset",
                transfer.asset,
                "--amount",
                transfer.amout,
                "--is_deposit",
                "true" if transfer.is_deposit else "false",
                "--nonce",
                transfer.nonce,
                "--private_key",
                self._private_key,
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )

    def positions(self, channel_id: str, account: str):
        subprocess.run(
            [
                self._cli_path,
                "positions",
                "--channel_id",
                channel_id,
                "--account",
                account,
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )

    def quote(self, channel_id: str, rfq_id: str, quote: Quote):
        """
        Send a quote through the given channel_id.
        The response will be readable through the channel output.
        """
        subprocess.run(
            [
                self._cli_path,
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
                "--is_put",
                "true" if quote.isPut else "false",
                "--is_taker_buy",
                "true" if quote.isTakerBuy else "false",
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
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )
