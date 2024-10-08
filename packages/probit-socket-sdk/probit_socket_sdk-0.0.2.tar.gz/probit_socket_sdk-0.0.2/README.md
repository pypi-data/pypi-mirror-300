# ProbitSocketSDK-python

## Installation

```bash
pip install probit_socket_sdk
```

## How to Use

1. Enter your API ID and Secret values ​​as shown below.
```bash
API_CLIENT_ID = '12345678'
API_CLIENT_SECRET = '1a2b3c4d5e6f7g8h'
```

2. Call the constructor of ProbitSDK.
```python
from probit_socket_sdk import ProBitSdk

id = "12345678"
secret = "1a2b3c4d5e6f7g8h"
sdk = ProBitSdk(id, secret)
```

3. You can call the functions below. More will be added if needed
```python
from probit_socket_sdk import CHANNEL_TYPE
from probit_socket_sdk import FILTER_TYPE

sdk.connect_market_data("BTC-USDT", [FILTER_TYPE.order_books_l0.name, FILTER_TYPE.order_books_l4.name, FILTER_TYPE.recent_trades.name, FILTER_TYPE.ticker.name])
sdk.connect_my_balance()
sdk.connect_open_order()
```

In the case of filter, you can set it as follows.
- order_books_l0
- order_books_l1
- order_books_l2
- order_books_l3
- order_books_l4
- ticker
- recent_trades

For market_id, an example would look like this: (ex, BTC-USDT)

See test.py for a detailed example.

