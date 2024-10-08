from argparse import ArgumentParser
from dataclasses import dataclass
import enum
import json
import logging as lg
import os
from pathlib import Path
import random
import subprocess as sp
import sys
import traceback as tb
from typing import (
    Any,
    Optional,
    Sequence
)

from . import (
    Address,
    run_snippet,
    server_set_up,
)
from ._impl import (
    address2str,
    parse_address,
)


LOG = lg.getLogger(__name__)


class Mode(enum.Enum):
    CLIENT = enum.auto()
    SERVER = enum.auto()


DEFAULT_SESSION = Path(".sock_python.json")


@dataclass
class Options:
    mode: Mode
    address: Address
    session: Optional[Path]
    log_level: int = lg.WARNING

    @property
    def settings_from_session(self) -> dict[str, Any]:
        if self.session and self.session.is_file():
            return json.loads(self.session.read_text("utf-8"))
        return {}

    @classmethod
    def from_args(cls, args: Sequence[str]) -> "Options":
        parser = ArgumentParser(
            description=(
                "Hosts an interactive Python session over a socket service; or connect "
                "to such a service to send a Python snippet to run, and receive "
                "outputs. In client mode, the Python code snippet to run is provided "
                "through standard input."
            )
        )
        parser.add_argument(
            "address",
            nargs="*",
            help=(
                "Address to either serve on or connect to. If the address takes the "
                "form [HOST]:PORT, then the connection is run over TCP/IP; the default "
                "host is localhost (not empty string!). Otherwise, the address is a "
                "path on the filesystem, and the session is run over UNIX sockets. "
                "It is fine to run without an address. In server mode, this starts "
                "on a randomly generated UNIX socket path. In client mode, without "
                "an explicit address, we look for the session file (see option "
                "--file) for an address to connect to. Failing to find one terminates "
                "the program with an error."
            )
        )
        parser.add_argument(
            "-s",
            "--serve",
            help=(
                "Run in server mode: standard input is ignored, execution carries "
                "on until SIGINT signal is received (Ctrl+C). Without this option, "
                "the program runs in client mode: code snippet is provided on "
                "standard input, the standard output and error of the snippet are "
                "delivered back to the corresponding streams, and any exception "
                "raised during the snippet execution is documented (with traceback) "
                "on standard error. The client program exits with code 0 if the "
                "snippet ran without issue, and with an error code on exception. "
            ),
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-f",
            "--session",
            help=(
                "Path to a JSON file describing the status of the server. If we "
                "are running as server, this file is written to as execution goes; "
                "if we run as client, it is read in to determine whether a server "
                "is running, and the address at which to contact it. If the value "
                "given to this argument is `-', the session file is ignored (not "
                "written up as server, and not read in as client). "
                f"By default, the session file is {DEFAULT_SESSION} "
            ),
            default=DEFAULT_SESSION,
        )
        parser.add_argument(
            "-v",
            "--verbosity",
            choices=["debug", "info", "warn", "warning", "error", "critical"],
            default="warning",
            help=(
                "Verbosity level. Can choose, from least to most verbose, "
                "between `critical', `error', `warning' (default), `info' "
                "and `debug'."
            )
        )

        ns = parser.parse_args(args)
        return cls(
            mode={True: Mode.SERVER, False: Mode.CLIENT}[ns.serve],
            address=parse_address(":".join(ns.address)),
            session=Path(ns.session) if ns.session != "-" else None,
            log_level=lg.getLevelName(ns.verbosity.upper())
        )


def determine_address(options: Options) -> Address:
    if options.address:
        return options.address
    settings = options.settings_from_session
    if "address" in settings:
        return parse_address(settings["address"])
    if options.mode == Mode.SERVER:
        LOG.warning("No address explicitly given. Will use a random UNIX socket path.")
        chars = "".join(chr(i) for i in range(ord('a'), ord('z') + 1))
        while True:
            address = "".join(random.choice(chars) for _ in range(8)) + ".sock"
            if not os.path.exists(address):
                return address
    lg.getLogger(__name__).critical(
        "No address was provided on command line, and " + (
            f"none could be determined from {options.session}. "
            if options.session
            else "no session file could be used to determine one. "
        ) + "Abort."
    )
    sys.exit(1)


def do_server(address: Address, session: Optional[Path]) -> None:
    LOG.debug("Running as server")
    with server_set_up(address, __name__) as (address_actual, serve):
        LOG.info(f"PID: {os.getpid()} | Address: {address_actual}")
        if session:
            LOG.info(f"Update session file {session}")
            session.write_text(json.dumps({
                "address": address2str(address_actual),
                "pid": os.getpid(),
            }))

        try:
            must_restart = serve({})
        except Exception:
            tb.print_exc()
            sys.exit(20)

    if must_restart:
        LOG.warning("Restart the server")
        sys.exit(
            sp.run([
                sys.executable,
                "-m",
                "sock_python",
                "--serve",
                "--session",
                (str(session) if session else "-"),
                address2str(address),
            ]).returncode
        )


def do_client(address: Address) -> None:
    LOG.debug("Running as client")
    LOG.info("Reading in code snippet")
    code = sys.stdin.read()
    captured, exception = run_snippet(address, code)
    LOG.debug("Code snippet execution complete")
    sys.stdout.write(captured)
    if exception:
        LOG.warning("Exception raised during snippet execution")
        sys.stderr.write(exception)
        sys.exit(10)
    sys.exit(0)


def main():
    options = Options.from_args(sys.argv[1:])
    lg.basicConfig(level=options.log_level, format="%(levelname)8s | %(message)s")
    address = determine_address(options)
    match options.mode:
        case Mode.SERVER:
            do_server(address, options.session)
        case Mode.CLIENT:
            do_client(address)
        case _:
            LOG.critical(f"No way yet to handle execution mode {options.mode.name}")
            sys.exit(2)


if __name__ == "__main__":
    main()
