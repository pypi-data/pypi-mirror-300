import json
import os
import pytest
import struct

from sock_python._impl import (
    Ack,
    Action,
    Control,
    handle_packet,
    json2packet,
    Output,
    Snippet,
)


def test_snippet():
    assert Snippet(code='print("heyhey")') == json2packet(
        '{"snippet": "print(\\\"heyhey\\\")"}'
    )


def test_output():
    assert Output(captured="asdf\n", exception="") == json2packet(
        '{"captured": "asdf\\n"}'
    )


def test_output_exception():
    assert Output(captured="", exception="asdfqwerty") == json2packet(
        '{"exception": "asdfqwerty"}'
    )


def test_output_both():
    assert Output(captured="asdf", exception="qwer") == json2packet(
        '{"captured": "asdf", "exception": "qwer"}'
    )


@pytest.mark.parametrize(
    "name,action",
    [
        ("stop", Action.STOP),
        ("status", Action.STATUS),
        ("restart", Action.RESTART),
    ]
)
def test_control(name, action):
    assert Control(action=action) == json2packet(f'{{"control": "{name}"}}')


@pytest.mark.parametrize(
    "name,action,response",
    [
        ("stop", Action.STOP, ""),
        ("restart", Action.RESTART, ""),
        ("status", Action.STATUS, '{\\"pid\\": 12345}'),
    ]
)
def test_ack(name, action, response):
    assert Ack(action=action, response=response.replace("\\", "")) == json2packet(
        f'{{"ack": "{name}", "response": "{response}"}}'
    )


class MockLog:

    def __init__(self):
        self.entries = {}

    def _append(self, level, msg):
        self.entries.setdefault(level, []).append(msg)

    def debug(self, msg):
        self._append("debug", msg)


@pytest.fixture
def log():
    return MockLog()


class MockConnection:

    def __init__(self):
        self.sent = []

    def send(self, bs):
        self.sent.append(bs)
        return len(bs)


@pytest.fixture
def conn():
    return MockConnection()


def check_packet_size(conn, i=1):
    assert len(conn.sent[i]) == struct.unpack(">I", conn.sent[i - 1])[0]


def test_handle_stop(log, conn):
    assert (True, False) == handle_packet(Control(action=Action.STOP), {}, conn, log)
    assert conn.sent[1] == json.dumps({"ack": "stop", "response": ""}).encode("utf-8")
    check_packet_size(conn)


def test_handle_restart(log, conn):
    assert (True, True) == handle_packet(Control(action=Action.RESTART), {}, conn, log)
    assert conn.sent[1] == json.dumps({"ack": "restart", "response": ""}).encode(
        "utf-8"
    )
    check_packet_size(conn)


def test_handle_status(log, conn):
    assert (False, False) == handle_packet(Control(action=Action.STATUS), {}, conn, log)
    assert conn.sent[1] == json.dumps(
        {"ack": "status", "response": json.dumps({"pid": os.getpid()})}
    ).encode("utf-8")
    check_packet_size(conn)


@pytest.fixture
def env():
    return {}


def test_handle_snippet(env, log, conn):
    Snippet(code="get('hey')\n").run(env, conn)
    assert conn.sent[1] == json.dumps(
        {"captured": "hey", "exception": ""}
    ).encode("utf-8")
    check_packet_size(conn)
