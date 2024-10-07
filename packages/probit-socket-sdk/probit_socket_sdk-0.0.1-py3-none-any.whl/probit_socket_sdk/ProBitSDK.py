from .WebSocketClient import WebSocketClient
from .Authentication import Authentication
import json

from .constant.channel_type import CHANNEL_TYPE


class ProBitSdk:
    __authentication: Authentication
    __webSocket: WebSocketClient

    def __init__(self, api_client_id, api_client_secret):
        self.__authentication = Authentication(api_client_id, api_client_secret)
        self.__webSocket = WebSocketClient()

    def get_cached_data(self, channel, market_id=None, filter=None):
        if channel == CHANNEL_TYPE.MARKET_DATA.value:
            return self.__webSocket.get_cached_market_data(market_id, filter)
        else:
            return self.__webSocket.get_cached_data(channel)

    def check_connection(self):
        if not self.__webSocket.connected():
            self.__webSocket.connect()

    def connect_market_data(self, market_id, filter_type):
        self.check_connection()

        self.__webSocket.connect_market_data(market_id, filter_type)

    def process_authentication(self):
        self.check_connection()

        if not self.__webSocket.authenticated():
            self.__webSocket.process_authentication(self.__authentication.get_token())

    def connect_my_balance(self):
        self.process_authentication()

        self.__webSocket.connect_balance()

    def connect_open_order(self):
        self.process_authentication()

        self.__webSocket.connect_open_order()



