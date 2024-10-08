# Sock Python: lightweight interactive Python sessions over a link

This package provides a server to execute given snippets of Python code, and relay selected results back to the client. The server works like an interactive Python session, taking inputs from client connections. It listens either to a streaming UNIX socket or to a TCP/IP port. Also included in this library is the client software for either issuing snippets for the server to run, or control the server instance remotely.

**For Jupyter fans**: you can understand this package as like a lightweight Python kernel mechanism, providing both the kernel and its client, in a Python programmatic form as well as simple command-line interface.

---

## **CRITICAL SECURITY WARNING**

While it is _possible_, one should be careful not to bind the server to an externally visible IP interface. This would grant unauthenticated execution access to the machine to the whole network -- a very easy infiltration path for somebody to take over control of the machine. To be very clear, **do not do this**:

```sh
# NOOOO! DO NOT DO THIS
python -m sock_python --serve 0.0.0.0:9887
# NOOOOOOO! DO NOT DO THIS EITHER
python -m sock_python --serve my.domain.name:9887
```

The preferred way to serve is through a UNIX socket:

```sh
# This is the safest.
python -m sock_python --serve local/path/to/socket.sock
```

Alternatively, one may bind to their loopback interface, although this grants access to all other users that may be using the machine:

```sh
# This is risky, do it only if you understand the consequences.
python -m sock_python --serve localhost:9887
# Equivalent command line:
python -m sock_python --serve :9887  # Empty is filled with localhost.
```

This latter form is most useful when using the server over a SSH tunnel.

**Final repeat: do not run the server bound to an external IP interface.**

---


## Installation

```sh
pip install sock_python
```

This package has no dependency.


## Usage

This is a client-server system that articulates an interactive Python session. The server runs the Python code sent over by the client, and relays back strings with which code invokes the `get` function.

### Command line interface (CLI)

To run the server, the part of the system that will run a sequence of Python snippets:

```sh
python -m sock_python --serve session.sock
```

The server will start listening on UNIX socket named `session.sock` in the current directory. It will also store this preferred session address in local file `.sock_python.json`. To change this session file, use option `-f`:

```sh
python -m sock_python -sf my_session.json session.sock
```

The server runs snippets forever. One can terminate the server by hitting `Ctrl+C`.

The client runs using the same command line, except for the `-s/--serve` command line option. The code snippet to send the server is provided at the standard input of the client: the unaware may feel that the client is stuck as it does nothing as it starts up. Type the code snippet, then **Ctrl+D** to have the client send it to the server. The snippet can get back some information from the server by invoking the `get()` function. Once the server is finished running the snippet, everything that the client `get`ted is printed to standard output. Here is a full example:

```sh
python -m sock_python session.sock
a = 5
get(f"{a * 3}")
b = 8
get(a + b)
<CTRL+D>
15 13
```

The client can take advantage of the session file to avoid typing in the server's address.

```sh
# Assuming the server wrote its coordinates in file my_session.json
python -m sock_python -f my_session.json < snippet.py
# Or even better, using the default session file
python -m sock_python
from textwrap import dedent
get(dedent("""\
    asdf
      qwer
    zxcv
"""))
<CTRL+D>
asdf
  qwer
zxcv
```

If the code snippet given by the client raises an exception, its traceback is relayed back and printed on the client's standard error stream. The client process then terminates with a non-zero exit code.

### Python usage

Running the server:

```python
from sock_python import server_set_up

# The session is captured in implicit process state, as well as the module namespace
# in which the Python snippets are run. This namespace is encapsulated in a dictionary.
env = {}
with server_set_up("local.sock") as (address, serve):
    print(address)  # Effective address being served on.

    # The serve function will service snippets forever! (Ctrl+C interrupts)
    serve(env)
```

A TCP/IP address in the form of a tuple `(host, port)` can be given instead of a UNIX socket path string. If such a TCP/IP address is provided with port number 0, the underlying operating system binds the server to an [ephemeral port](https://en.wikipedia.org/wiki/Ephemeral_port), and this final address is what is captured by the `address` variable above. Naturally, in most cases, as is the case above, `address` takes the exact same value as the argument to `server_set_up`.

The client (in another thread or process):

```python
from sock_python import run_snippet

snippet = """\
get(1 << 20)
"""
output, exception = run_snippet("local.sock", snippet)
```

Once again, a TCP/IP tuple address can be used instead. `output` contains the concatenation of all the `get`ted strings. If the snippet runs without any runaway exception, `exception` is the empty string; otherwise, it is a string rendering of the exception's traceback.

In addition to running code snippets, an alternative client interface can be used to control the server process remotely.

```python
from sock_python import Action, control

response = control("local.sock", Action.STOP)
```

The possible actions one can perform through this control interface:

1. `Action.STOP`: terminates the server, which will then exit gracefully. `response` is an empty dictionary.
1. `Action.RESTART`: restarts the server process, which will re-bind to the same address, but restart from a fresh process space. This is useful to reset the session to its initial state. `response` is an empty dictionary.
1. `Action.STATUS`: returns some status information about the server, provided as the `response` dictionary.


## Some gotchas

**The server is a single-threaded process**

Therefore, it runs one snippet at a time, and only when done then processes further connections. If your snippet falls into an endless loop, the server will need restarting by interruption or process termination through the operating system services.
