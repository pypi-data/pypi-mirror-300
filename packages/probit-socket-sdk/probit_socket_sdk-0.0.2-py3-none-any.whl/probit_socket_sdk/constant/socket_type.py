from enum import Enum


class SOCKET_TYPE(Enum):
    AUTHORIZATION = "authorization"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
