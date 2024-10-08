import logging as lg
from pathlib import Path
import pytest

from sock_python.__main__ import (
    DEFAULT_SESSION,
    Mode,
    Options,
)


@pytest.mark.parametrize(
    "expected,args",
    [
        (
            Options(Mode.CLIENT, "sock.python", DEFAULT_SESSION),
            ["sock.python"],
        ),
        (
            Options(Mode.CLIENT, "", DEFAULT_SESSION),
            [],
        ),
        (
            Options(Mode.SERVER, ("localhost", 9887), Path("heyhey")),
            ["-f", "heyhey", "-s", "localhost:9887"],
        ),
        (
            Options(Mode.SERVER, ("", 12345), None),
            ["--serve", "--session", "-", ":12345"],
        ),
        (
            Options(Mode.CLIENT, ("localhost", 9887), DEFAULT_SESSION),
            ["localhost", "9887"]
        ),
        (
            Options(Mode.CLIENT, "", DEFAULT_SESSION, log_level=lg.DEBUG),
            ["-v", "debug"]
        ),
        (
            Options(Mode.CLIENT, "", DEFAULT_SESSION, log_level=lg.INFO),
            ["-v", "info"]
        ),
        (
            Options(Mode.CLIENT, "", DEFAULT_SESSION, log_level=lg.WARNING),
            ["-v", "warning"]
        ),
        (
            Options(Mode.CLIENT, ("", 9887), DEFAULT_SESSION, log_level=lg.WARNING),
            ["--verbosity", "warn", ":9887"]
        ),
        (
            Options(Mode.CLIENT, "", DEFAULT_SESSION, log_level=lg.ERROR),
            ["-v", "error"]
        ),
        (
            Options(Mode.CLIENT, "", DEFAULT_SESSION, log_level=lg.CRITICAL),
            ["-v", "critical"]
        ),
    ]
)
def test_args(expected, args):
    assert expected == Options.from_args(args)
