from websocket import WebSocketApp
from .constant.filter_type import FILTER_TYPE
from .constant.socket_type import SOCKET_TYPE
from .constant.channel_type import CHANNEL_TYPE
from .constant.type import WEBSOCKET_CONNECTION
from threading import Thread, Event
import ssl
import time
import json


class WebSocketClient:
    __wst: Thread
    __client: WebSocketApp
    __connected: bool
    __authenticated: bool
    __maximum_cached: int
    __cached_data: {}
    __connection_event = Event()
    __authentication_event = Event()
    __market_data_event = Event()
    __balance_event = Event()
    __open_order_event = Event()

    def __init__(self):
        self.__connected = False
        self.__authenticated = False
        self.__maximum_cached = 100
        self.__cached_data = {}

    def connected(self):
        return self.__connected

    def authenticated(self):
        return self.__authenticated

    def on_message(self, client, message):
        json_object = json.loads(message)
        if "type" in json_object and json_object["type"] == SOCKET_TYPE.AUTHORIZATION.value:
            if json_object["result"] == 'ok':
                self.__authenticated = True
            self.__authentication_event.set()
        else:
            if "channel" in json_object and json_object["channel"] == CHANNEL_TYPE.MARKET_DATA.value:

                # current_time_seconds = time.time()
                # milliseconds = int((current_time_seconds - int(current_time_seconds)) * 100)
                # print(f"{time.strftime("%H:%M:%S", time.localtime(current_time_seconds))}.{milliseconds} : {json_object}")
                for f in FILTER_TYPE._member_names_:
                    if f in json_object:
                        if FILTER_TYPE.order_books_l0.value <= FILTER_TYPE[f].value <= FILTER_TYPE.order_books_l4.value:
                            for v in json_object[f]:
                                if v["side"] == "buy":
                                    if v["quantity"] == '0':
                                        self.__cached_data[json_object["channel"]][json_object["market_id"]][f][
                                            "buy"].pop(
                                            v["price"], None)
                                    else:
                                        self.__cached_data[json_object["channel"]][json_object["market_id"]][f]["buy"][
                                            v["price"]] = v["quantity"]
                                else:
                                    if v["quantity"] == '0':
                                        self.__cached_data[json_object["channel"]][json_object["market_id"]][f][
                                            "sell"].pop(
                                            v["price"], None)
                                    else:
                                        self.__cached_data[json_object["channel"]][json_object["market_id"]][f]["sell"][
                                            v["price"]] = v["quantity"]
                        elif FILTER_TYPE.ticker.value == FILTER_TYPE[f].value:
                            self.__cached_data[json_object["channel"]][json_object["market_id"]][f].append(
                                json_object[f])
                        else:
                            for v in json_object[f]:
                                if len(self.__cached_data[json_object["channel"]][json_object["market_id"]][
                                           f]) >= self.__maximum_cached:
                                    del self.__cached_data[json_object["channel"]][json_object["market_id"]][f][0]
                                self.__cached_data[json_object["channel"]][json_object["market_id"]][f].append(v)
                self.__market_data_event.set()
            elif json_object["channel"] == CHANNEL_TYPE.BALANCE.value:
                self.__balance_event.set()
                self.__cached_data[json_object["channel"]] = json_object["data"]
            elif json_object["channel"] == CHANNEL_TYPE.OPEN_ORDER.value:
                self.__open_order_event.set()
                self.__cached_data[json_object["channel"]] = json_object["data"]

    def on_error(self, client, error):
        print(error)
        self.__connection_event.set()
        self.__connected = False

    def on_close(self, client, close_status_code, close_msg):
        print("WebSocket Closed")
        self.__connection_event.set()
        self.__connected = False

    def on_open(self, client):
        print("WebSocket Connected")
        self.__connection_event.set()
        self.__connected = True

    def connect(self):
        self.__client = WebSocketApp(WEBSOCKET_CONNECTION,
                                     on_open=self.on_open,
                                     on_message=self.on_message,
                                     on_error=self.on_error,
                                     on_close=self.on_close)
        self.__wst = Thread(target=self.__client.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        self.__wst.daemon = True
        self.__wst.start()

        self.__connection_event.wait()

        if not self.__connected:
            raise RuntimeError('Failed to Connect')

    def get_cached_market_data(self, market_id, filter):
        if CHANNEL_TYPE.MARKET_DATA.value not in self.__cached_data \
                or market_id not in self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value] \
                or filter not in self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id]:
            return {"data": {}}

        if FILTER_TYPE.order_books_l0.value <= FILTER_TYPE[filter].value <= FILTER_TYPE.order_books_l4.value:
            data = []
            for obj in self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][filter]["buy"]:
                data.append({
                    "side": "buy",
                    "price": obj,
                    "quantity": self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][filter]["buy"][obj]
                })

            for obj in self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][filter]["sell"]:
                data.append({
                    "side": "sell",
                    "price": obj,
                    "quantity": self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][filter]["sell"][obj]
                })
            return {"data": data}
        else:
            return {"data": self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][filter]}

    def get_cached_data(self, channel):
        if channel == CHANNEL_TYPE.BALANCE.value:
            data = []
            for bal in self.__cached_data[channel]:
                data.append({
                    "currency_id": bal,
                    "total": self.__cached_data[channel][bal]["total"],
                    "available": self.__cached_data[channel][bal]["available"]
                })
            return data
        elif channel == CHANNEL_TYPE.OPEN_ORDER.value:
            return self.__cached_data[channel]

    def connect_market_data(self, market_id, filter_type):
        if CHANNEL_TYPE.MARKET_DATA.value not in self.__cached_data:
            self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value] = {}

        if market_id not in self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value]:
            self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id] = {}

        for f in filter_type:
            if f not in self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id]:
                if FILTER_TYPE.order_books_l0.value <= FILTER_TYPE[f].value <= FILTER_TYPE.order_books_l4.value:
                    self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][f] = {
                        "buy": {},
                        "sell": {}
                    }
                else:
                    self.__cached_data[CHANNEL_TYPE.MARKET_DATA.value][market_id][f] = []

        json_obj = {
            "type": SOCKET_TYPE.SUBSCRIBE.value,
            "channel": CHANNEL_TYPE.MARKET_DATA.value,
            "interval": 500,
            "market_id": market_id,
            "filter": filter_type
        }

        message = json.dumps(json_obj)

        self.__client.send(message)
        self.__market_data_event.wait()

    def process_authentication(self, token):
        json_obj = {
            "type": SOCKET_TYPE.AUTHORIZATION.value,
            "token": token
        }

        message = json.dumps(json_obj)

        self.__client.send(message)
        self.__authentication_event.wait()

        if not self.__authenticated:
            raise RuntimeError('Failed to Authenticate')

    def connect_balance(self):
        if CHANNEL_TYPE.BALANCE.value not in self.__cached_data:
            self.__cached_data[CHANNEL_TYPE.BALANCE.value] = {}

        json_obj = {
            "type": SOCKET_TYPE.SUBSCRIBE.value,
            "channel": CHANNEL_TYPE.BALANCE.value
        }

        message = json.dumps(json_obj)

        self.__client.send(message)
        self.__balance_event.wait()

    def connect_open_order(self):
        if CHANNEL_TYPE.OPEN_ORDER.value not in self.__cached_data:
            self.__cached_data[CHANNEL_TYPE.OPEN_ORDER.value] = {}

        json_obj = {
            "type": SOCKET_TYPE.SUBSCRIBE.value,
            "channel": CHANNEL_TYPE.OPEN_ORDER.value
        }

        message = json.dumps(json_obj)

        self.__client.send(message)
        self.__open_order_event.wait()
