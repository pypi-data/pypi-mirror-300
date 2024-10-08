from contextlib import closing, contextmanager
from dataclasses import dataclass, field
from enum import auto, Enum
from hashlib import md5
import logging as lg
import json
import os
import socket
import struct
import sys
import traceback as tb
from typing import (
    Any,
    Callable,
    Iterator,
    Mapping,
    Protocol,
    Union
)


Address = Union[str, tuple[str, int]]
NEWLINE = "\n"


def parse_address(raw: str) -> Address:
    host, *rest = raw.split(":")
    match rest:
        case []:
            return host
        case [port]:
            return (host, int(port))
        case _:
            raise ValueError("Illegal address")


def address2str(address: Address) -> str:
    if isinstance(address, tuple):
        try:
            host, port = address
            if isinstance(host, str) and isinstance(port, int):
                return f"{host}:{port}"
        except ValueError:
            pass
    elif isinstance(address, str):
        return address
    raise ValueError(f"Improper address: {repr(address)}")


ObjectRaw = Mapping[str, Union[str, int, bool, None]]


class Packet(Protocol):

    def to_raw(self) -> ObjectRaw: ...
    def describe(self) -> str: ...


def format_frame(ss: tb.FrameSummary, lines_snippet: list[str]) -> str:
    NO_CODE = '<no code>'
    if ss.line:
        line_code = ss.line
    elif ss.filename == "Snippet" and ss.lineno:
        line_code = lines_snippet[ss.lineno - 1]
    else:
        line_code = NO_CODE

    if line_code != NO_CODE and ss.colno and ss.end_colno:
        underscore = "\n    " + " " * ss.colno + "^" * (ss.end_colno - ss.colno)
    else:
        underscore = ""

    return f"""\
{"File " if ss.filename != "Snippet" else ""}{ss.filename}, line {ss.lineno}, \
in {ss.name}:
    {line_code}{underscore}
"""


@dataclass
class Snippet:
    code: str

    def to_raw(self) -> ObjectRaw:
        return {"snippet": self.code}

    @property
    def md5(self) -> str:
        return md5(self.code.encode("utf-8")).hexdigest()

    def describe(self) -> str:
        return (
            f"Snippet: {len(self.code)} chars of code, "
            f"MD5 {self.md5}"
        )

    def run(self, env: dict, conn: socket.socket) -> None:
        output = Output(captured="")
        env["get"] = output.get

        try:
            compiled = compile(self.code, "Snippet", "exec")
            exec(compiled, env, env)
        except KeyboardInterrupt:
            raise
        except Exception:
            ex_type, ex_value, ex_tb = sys.exc_info()
            frames = tb.extract_tb(ex_tb)
            while frames:
                if frames[0].filename == "Snippet":
                    break
                del frames[0]
            lines_snippet = self.code.split("\n")
            output.exception = "".join(
                format_frame(frame, lines_snippet)
                for frame in frames
            ) + f"{ex_type.__name__ if ex_type else '???'}: {str(ex_value)}"

        output.consolidate()
        send_packet(output, conn)


@dataclass
class Output(Packet):
    captured: str = ""
    exception: str = ""
    _captured: list[str] = field(default_factory=list)

    def to_raw(self) -> ObjectRaw:
        return {
            "captured": self.captured,
            "exception": self.exception,
        }

    def describe(self) -> str:
        fields = []
        if self.captured:
            fields.append(f"captured {len(self.captured)} chars")
        if self.exception:
            fields.append(f"exception [{self.exception.strip().split(NEWLINE)[-1]}]")
        if not fields:
            fields.append("(empty)")
        return f"Output: {' | '.join(fields)}"

    def get(self, obj: Any) -> None:
        self._captured.append(str(obj))

    def consolidate(self) -> str:
        self.captured = "".join(self._captured)
        return self.captured


class Action(Enum):
    STOP = auto()
    RESTART = auto()
    STATUS = auto()

    @classmethod
    def from_name(cls, name: str) -> "Action":
        name_upper = name.upper()
        if not hasattr(cls, name_upper):
            raise ValueError(f"Action name {name} has no correspondance")
        return getattr(cls, name_upper)


@dataclass
class Control(Packet):
    action: Action

    def to_raw(self) -> ObjectRaw:
        return {"control": self.action.name.lower()}

    def describe(self) -> str:
        return f"Control: {self.action.name}"

    def handle(self, conn: socket.socket) -> tuple[bool, bool]:
        reply = Ack(action=self.action)
        must_stop = False
        must_restart = False
        match self.action:
            case Action.STOP:
                must_stop = True
            case Action.RESTART:
                must_stop, must_restart = True, True
            case Action.STATUS:
                reply.response = json.dumps({"pid": os.getpid()})

        send_packet(reply, conn)
        return must_stop, must_restart


@dataclass
class Ack(Packet):
    action: Action
    response: str = ""

    def to_raw(self) -> ObjectRaw:
        return {"ack": self.action.name.lower(), "response": self.response}

    def describe(self) -> str:
        return f"Ack: {self.action.name} [{self.response}]"


def json2packet(code: str) -> Packet:
    obj = json.loads(code)
    if "snippet" in obj:
        return Snippet(code=obj["snippet"])
    elif "captured" in obj or "exception" in obj:
        return Output(**obj)
    elif "control" in obj:
        return Control(action=Action.from_name(obj["control"]))
    elif "ack" in obj:
        return Ack(action=Action.from_name(obj["ack"]), response=obj["response"])
    else:
        raise ValueError("Invalid packet string")


def send_packet(packet: Packet, sock: socket.socket) -> None:
    code_packet = json.dumps(packet.to_raw()).encode("utf-8")
    assert len(code_packet) <= (1 << 32) - 1
    to_send = [struct.pack(">I", len(code_packet)), code_packet]
    while to_send:
        n = sock.send(to_send[0])
        to_send[0] = to_send[0][n:]
        if not to_send[0]:
            del to_send[0]


@dataclass
class PacketIncomplete(Exception):
    num_bytes: int


def recv_packet(sock: socket.socket) -> Packet:
    total_received = 0

    def recv_exactly(n: int) -> bytes:
        nonlocal total_received
        received = []
        while n > 0:
            bs = sock.recv(n)
            if not bs:
                raise OSError("Transit interrupted unduly")
            assert len(bs) > 0
            total_received += len(bs)
            n -= len(bs)
            received.append(bs)
        return b"".join(received)

    try:
        len_json, = struct.unpack(">I", recv_exactly(4))
        return json2packet(recv_exactly(len_json).decode("utf-8"))
    except OSError:
        raise PacketIncomplete(num_bytes=total_received)


def address2family(address: Address) -> socket.AddressFamily:
    if isinstance(address, tuple):
        return socket.AF_INET
    elif isinstance(address, str):
        return socket.AF_UNIX
    else:
        raise ValueError(f"No socket family to handle address {address}")


def handle_packet(
    packet: Packet,
    env: dict,
    conn: socket.socket,
    log: lg.Logger
) -> tuple[bool, bool]:
    if isinstance(packet, Snippet):
        log.debug("Running snippet")
        packet.run(env, conn)
        return False, False
    elif isinstance(packet, Control):
        log.debug("Handling control request")
        return packet.handle(conn)
    else:
        log.error(
            f"Packet [{packet.describe()}] ignored, unacceptable from "
            "ground state"
        )
        return False, False


RunServer = Callable[[dict], bool]


@contextmanager
def server_set_up(
    address,
    name_logger: str = f"{__name__}.server"
) -> Iterator[tuple[Address, RunServer]]:
    log = lg.getLogger(name_logger)
    sock_service = socket.socket(address2family(address), socket.SOCK_STREAM)
    sock_service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_service.bind(address)
    address_effective = sock_service.getsockname()

    try:
        sock_service.listen()
        log.info(f"Sock Python service listening on {address_effective}")

        def serve(env: dict) -> bool:
            log.debug("Service starts")
            try:
                while True:
                    conn, peer = sock_service.accept()
                    try:
                        packet = recv_packet(conn)
                        log.info(f"From {peer or '[--]'}> {packet.describe()}")
                        must_stop, must_restart = handle_packet(packet, env, conn, log)
                        if must_stop:
                            return must_restart
                    except PacketIncomplete as err:
                        log.error(
                            f"From {peer or '[--]'}> incomplete packet, "
                            f"only {err.num_bytes} bytes received"
                        )
                    finally:
                        conn.close()
            except KeyboardInterrupt:
                log.info("Interrupted: forcing exit")
                return False
            finally:
                log.debug("Service stops")

        yield address_effective, serve
    finally:
        sock_service.close()
        if sock_service.family == socket.AF_UNIX:
            os.unlink(address)


def _connect(address: Address) -> socket.socket:
    sock = socket.socket(address2family(address), socket.SOCK_STREAM, 0)
    sock.connect(address)
    return sock


def control(address: Address, action: Action) -> Mapping[str, Any]:
    with closing(sock := _connect(address)):
        send_packet(Control(action=action), sock)
        ack = recv_packet(sock)
    if not isinstance(ack, Ack):
        raise TypeError(
            "Expected to receive an Ack packet as reply to a Control packet,"
            f"but got {ack.describe()}"
        )
    if ack.action != action:
        raise RuntimeError(
            f"Expected acknowledgment of action {action.name},"
            f"got {ack.action.name}"
        )
    return json.loads(ack.response or "{}")


def run_snippet(address: Address, code: str) -> tuple[str, str]:
    with closing(sock := _connect(address)):
        send_packet(Snippet(code=code), sock)
        output = recv_packet(sock)
    if not isinstance(output, Output):
        raise TypeError(
            "Expected to receive an Output packet as reply to a Snippet packet,"
            f"but got {output.describe()}"
        )
    return output.captured, output.exception
