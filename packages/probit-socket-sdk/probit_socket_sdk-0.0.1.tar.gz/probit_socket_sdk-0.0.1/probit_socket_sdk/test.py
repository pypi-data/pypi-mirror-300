from ProBitSDK import ProBitSdk
from constant.channel_type import CHANNEL_TYPE
from constant.filter_type import FILTER_TYPE
import time

id = "12345678"
secret = "1a2b3c4d5e6f7g8h"

sdk = ProBitSdk(id, secret)
sdk.connect_market_data("BTC-USDT", [FILTER_TYPE.order_books_l0.name, FILTER_TYPE.order_books_l4.name,
                                    FILTER_TYPE.recent_trades.name, FILTER_TYPE.ticker.name])
sdk.connect_my_balance()
sdk.connect_open_order()

print(
    f"order_books_l0: {sdk.get_cached_data(CHANNEL_TYPE.MARKET_DATA.value, "BTC-USDT", FILTER_TYPE.order_books_l0.name)}")
print(f"ticker: {sdk.get_cached_data(CHANNEL_TYPE.MARKET_DATA.value, "BTC-USDT", FILTER_TYPE.ticker.name)}")
print(
    f"recent_trade: {sdk.get_cached_data(CHANNEL_TYPE.MARKET_DATA.value, "BTC-USDT", FILTER_TYPE.recent_trades.name)}")
print(f"balance: {sdk.get_cached_data(CHANNEL_TYPE.BALANCE.value)}")
print(f"open_order: {sdk.get_cached_data(CHANNEL_TYPE.OPEN_ORDER.value)}")
