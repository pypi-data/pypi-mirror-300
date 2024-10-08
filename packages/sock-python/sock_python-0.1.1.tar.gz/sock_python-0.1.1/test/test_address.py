import pytest
import socket

from sock_python._impl import address2family, address2str, parse_address


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("", ""),
        ("just_name", "just_name"),
        ("path/to/unix/socket", "path/to/unix/socket"),
        (":0", ("", 0)),
        ("localhost:9887", ("localhost", 9887)),
        (":12345", ("", 12345)),
        ("192.168.32.21:7654", ("192.168.32.21", 7654)),
    ]
)
def test_address(raw, expected):
    assert expected == parse_address(raw)


@pytest.mark.parametrize(
    "family,address",
    [
        (socket.AF_UNIX, "test.sock"),
        (socket.AF_INET, ("localhost", 9887)),
    ]
)
def test_address2family(family, address):
    assert family == address2family(address)


@pytest.mark.parametrize(
    "rep,address",
    [
        ("test.sock", "test.sock"),
        ("/path/to/socket", "/path/to/socket"),
        ("localhost:9887", ("localhost", 9887)),
        (":34567", ("", 34567)),
    ]
)
def test_address2str(rep, address):
    assert rep == address2str(address)
