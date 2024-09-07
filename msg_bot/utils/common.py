import threading
from typing import Literal, Text

from ksuid import Ksuid


def gen_id(type: Literal["org", "conv", "msg", "usr"]) -> Text:
    return f"{type}_{Ksuid()}"


class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def value(self):
        with self._lock:
            return self._value
