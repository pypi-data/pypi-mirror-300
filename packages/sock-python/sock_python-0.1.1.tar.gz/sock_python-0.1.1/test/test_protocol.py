import json
from queue import Queue
import pytest
import random

from sock_python._impl import (
    Ack,
    Action,
    Control,
    Output,
    recv_packet,
    send_packet,
    Snippet,
)


def random_length(max_length: int) -> int:
    return random.randint(1, int(1.5 * max_length))


class MockSockets:

    def __init__(self):
        self._q = Queue()
        self._current = b""

    def send(self, bs: bytes) -> int:
        n = random_length(len(bs))
        self._q.put(bs[:n])
        return n

    def recv(self, n: int) -> bytes:
        n = random_length(n)
        if not self._current:
            self._current = self._q.get(timeout=0.)
        r = self._current[:n]
        self._current = self._current[n:]
        return r


@pytest.fixture
def conn():
    return MockSockets()


@pytest.mark.parametrize(
    "packet",
    [
        Snippet(code="asdfqwerty"),
        Output(captured="zxcvasdfqwer", exception="qwepoirsxb"),
        *[Control(action=action) for action in Action],
        Ack(action=Action.STATUS, response=json.dumps({"pid": 4567})),
    ]
)
def test_transmit(packet, conn):
    send_packet(packet, conn)
    assert packet == recv_packet(conn)
