import asyncio
import json
import os
import signal
import sys
import time
from ryskV12.models import Quote, Request, is_json_rpc_response, is_request
from ryskV12.client import Rysk, Env

private_key = ""
public_address = "0x50DdD5c84387a3B7836fAE45A4AD7499Bb10Bb24"
asset = "0xb67bfa7b488df4f2efa874f4e59242e9130ae61f"

def price_it(public_address: str, req: Request) -> Quote:
    # ...your magic goes here
    price = 4
    return Quote(
        req.asset,
        req.chainId,
        req.expiry,
        req.isPut,
        False,
        public_address,
        str(int(time.time() * 1000)),
        f"{price}000000000000000000",
        req.quantity,
        req.strike,
        int(time.time()) + 30,
        req.usd,
    )


async def process_rfqs():
    rysk_sdk = Rysk(env=Env.TESTNET, private_key=private_key, v12_cli_path="./ryskV12cli")
    maker_chan = "maker__py"
    rfq_chan = f'{asset}__py'
    try:
        asyncio.create_task(rysk_sdk.execute_async(rysk_sdk.connect_args(maker_chan, "maker")))

        def process_rfq(payload: bytes):
            # payload = str(payload)
            if payload == b'\n':
                return
            print(str(payload))
            try:
                data = json.loads(payload)
                if is_json_rpc_response(data):
                    request_id = data["id"]
                    result = data["result"]
                    if is_request(result):
                        quote = price_it(public_address, Request(
                            result['asset'],
                            result['assetName'],
                            result['chainId'],
                            result['expiry'],
                            result['isPut'],
                            result['quantity'],
                            result['strike'],
                            result['taker'],
                            result['usd'],
                        ))
                        cmd = rysk_sdk.quote_args(maker_chan, request_id, quote)
                        proc = rysk_sdk.execute(cmd)
                        print(proc.stdout.readlines())
                        print(proc.stderr.readlines())

            except Exception as e:
                print("error")
                print(e)

        await rysk_sdk.execute_async(rysk_sdk.connect_args(rfq_chan, f"rfqs/{asset}"), process_rfq)
    except Exception as e:
        print(e)
    finally:
        rysk_sdk.execute(rysk_sdk.disconnect_args(maker_chan))
        rysk_sdk.execute(rysk_sdk.disconnect_args(rfq_chan))

def handle_sig(sig, frame):
    os.remove(f"/tmp/{asset}__py.sock")
    os.remove("/tmp/maker__py.sock")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sig)
    asyncio.run(process_rfqs())