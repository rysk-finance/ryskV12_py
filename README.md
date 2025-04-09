# Rysk V12 Python SDK

Python wrapper for ryskv12-cli

## Setup

1.  **Ensure Python 3.12+ is installed.**
2.  **Install the required dependencies:**
    ```bash
    poetry install
    ```
3.  **Download the `ryskV12` CLI:** Navigate to [https://github.com/rysk-finance/ryskV12-cli/releases](https://github.com/rysk-finance/ryskV12-cli/releases) and download the latest release into the same directory where you will be using this SDK, naming it `ryskV12`. Ensure it has execute permissions.

## Run

### Instantiation

```python
from rysk_sdk import Rysk, Env

private_key = "YOUR_PRIVATE_KEY"  # Replace with your actual private key
env = Env.TESTNET  # Choose your environment: Env.LOCAL, Env.TESTNET, Env.MAINNET
rysk_sdk = Rysk(env=env, private_key=private_key, v12_cli_path="./ryskV12")  # Optional CLI path
```

### Create a Connection

```python
from rysk_sdk import Rysk, Env
from models import JSONRPCResponse

def response_handler(response: JSONRPCResponse):
    print(f"Received response: {response}")
    # Handle the JSON RPC response here
    # This is purposely left very generic so you can have your own implementation.
    # A few options are:
    # - Subscriber Pattern
    # - Message Queue
    # - Immediate Callback
    # - Streams

channel_id = "my-unique-channel-id"
uri = "/ws/0x..."  # Example websocket endpoint (replace with actual asset address)

rysk_sdk.connect(channel_id, uri, response_handler)
```

### Approve USDC Spending


```python
approval_channel_id = "approval-channel"
chain_id = 84532
amount = "1000000"

rysk_sdk.approve(approval_channel_id, chain_id, amount)
```

### List USDC Balances

```python
maker_channel = "maker-channel"
account = "0xabc"

rysk_sdk.balances(maker_channel, account)
```

### Deposit / Withdraw

```python
from models import Transfer

maker_channel = "maker-channel"
transfer_details = Transfer(
    amout="500000",
    asset="0x...",  # The asset address
    chain_id=84532,
    is_deposit=True,
    nonce="some-unique-nonce",
)

rysk_sdk.transfer(maker_channel, transfer_details)
```


### List Positions 

```python
maker_channel = "maker-channel"
account = "0xabc"

rysk_sdk.positions(maker_channel, account)
```

### Send a Quote


```python
from models import Quote

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

rysk_sdk.quote(maker_channel, request_id, quote_details)
```