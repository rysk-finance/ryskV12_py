# Rysk V12 Python SDK

Python wrapper for ryskV12 cli

## Setup

1.  **Ensure Python 3.11+ is installed.**
2.  **Install the required dependencies:**
    ```bash
    poetry add ryskV12
    ```
3.  **Download the `ryskV12` CLI:**
    Navigate to https://github.com/rysk-finance/ryskV12-cli/releases/latest and download the latest release in the root directory of your project as `ryskV12`.

## Run

### Instantiation

```python
from ryskV12.client import Rysk, Env

private_key = "YOUR_PRIVATE_KEY"
env = Env.TESTNET
rysk_sdk = Rysk(env=env, private_key=private_key, v12_cli_path="/path/to/ryskV12")  # Optional CLI path
```

### Create a Connection

```python

def response_handler(response: bytes):
    print(f"Received response: {response.strip()}")


channel_id = "rfqs_listener"
uri = "/rfqs/0x..."  # Example websocket endpoint (replace with actual asset address)

proc = rysk_sdk.execute_async(rysk_sdk.connect_args(channel_id, uri), response_handler)
```

### Approve USDC Spending

```python
chain_id = 84532
amount = "1000000"
rpc_url= "https://rpc..."

proc = rysk_sdk.execute(rysk_sdk.approve_args(chain_id, amount, rpc_url))
```

### List USDC Balances

```python
maker_channel = "maker-channel"
account = "0xabc"

proc = rysk_sdk.execute(rysk_sdk.balances_args(maker_channel, account))
```

### Deposit / Withdraw

```python
from ryskV12.models import Transfer

maker_channel = "maker-channel"
transfer_details = Transfer(
    amout="500000",
    asset="0x...",  # The asset address
    chain_id=84532,
    is_deposit=True,
    nonce="some-unique-nonce",
)
proc = rysk_sdk.execute(rysk_sdk.transfer_args(maker_channel, transfer_details))
```

### List Positions

```python
maker_channel = "maker-channel"
account = "0xabc"

proc = rysk_sdk.execute(rysk_sdk.positions_args(maker_channel, account))
```

### Send a Quote

```python
from ryskV12.models import Quote

maker_channel = "maker-channel"
request_id = "some-uuid-from-server"
quote_details = Quote(
    assetAddress="0x...",
    chainId=84532,
    expiry=1678886400,
    isPut=False,
    isTakerBuy=True,
    maker="0x...",
    nonce="another-unique-nonce",
    price="0.01",
    quantity="1",
    strike="1000000",
    validUntil=1678886460,
)

proc = rysk_sdk.execute(rysk_sdk.quote_args(maker_channel, request_id, quote_details))
```

## Example

```python
import asyncio
import json
import time
from ryskV12.models import Quote, is_json_rpc_response, is_request
from ryskV12.client import Rysk, Env

private_key = ""
public_address = ""
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
        req.collateralAsset
    )

async def process_rfqs():
    rysk_sdk = Rysk(env=Env.TESTNET, private_key=private_key)
    maker_chan = "maker__py"
    rfq_chan = f'{asset}__py'
    try:
        asyncio.create_task(rysk_sdk.execute_async(rysk_sdk.connect_args(maker_chan, "maker")))
        def process_rfq(payload: bytes):
            # print(payload)
            if payload == b'\n':
                return
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
                            result['collateralAsset']
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

```
