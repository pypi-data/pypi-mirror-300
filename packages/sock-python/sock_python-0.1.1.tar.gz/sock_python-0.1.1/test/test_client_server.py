from contextlib import closing, contextmanager
import logging as lg
import multiprocessing as mp
import os
import stat
import time

from sock_python._impl import (
    Action,
    control,
    run_snippet,
    server_set_up,
)


TEST_SOCK = "test.sock"


def check_socket_exists():
    if not os.path.exists(TEST_SOCK):
        return False
    return stat.S_ISSOCK(os.stat(TEST_SOCK).st_mode)


class Timeout(Exception):
    pass


def wait_for_test_socket(timeout):
    moment_start = time.time()
    while time.time() - moment_start <= timeout:
        if check_socket_exists():
            return
    raise Timeout()


def run_server():
    lg.basicConfig(level=lg.DEBUG)
    with server_set_up(TEST_SOCK) as (_, serve):
        serve({})


@contextmanager
def server():
    assert not check_socket_exists()

    with closing(process := mp.Process(target=run_server)):
        try:
            process.start()
            wait_for_test_socket(5.)
            yield process
        finally:
            if process.pid and process.exitcode is None:
                process.terminate()
                process.join(timeout=3.)
                if process.exitcode is None:
                    process.kill()
            if check_socket_exists():
                os.unlink(TEST_SOCK)


def test_stop_server():
    with server() as process:
        assert {} == control(TEST_SOCK, Action.STOP)
        process.join(5.)
        if process.exitcode is None:
            raise Timeout()


def test_session_no_problem():
    with server():
        output, traceback = run_snippet(TEST_SOCK, "get('hey')\na = 8\nget('ho\\n')\n")
        assert not traceback
        assert "heyho\n" == output
        output, traceback = run_snippet(TEST_SOCK, "b = 9\n")
        assert not output
        assert not traceback
        output, traceback = run_snippet(TEST_SOCK, "get(a + b)\n")
        assert "17" == output
        assert not traceback


def test_exception_no_kill():
    with server():
        output, traceback = run_snippet(TEST_SOCK, "ll = [1, 2, 8]\nget(ll.index(0))\n")
        assert not output
        assert traceback.startswith("Snippet, line 2, in <module>:")
        assert traceback.endswith("ValueError: 0 is not in list")
        output, traceback = run_snippet(TEST_SOCK, "a = 9\nget(7 * a)\n")
        assert "63" == output
        assert not traceback
