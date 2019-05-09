# Standard Library imports
from queue import Queue

# Pip dependency imports
import pytest

# Test fixture containing the socket client DUT
@pytest.fixture
def client_conn():
    from transvenous_pacing_gui import client

    return client.Client(port=25565)

# Test fixture containing the socket server DUT
@pytest.fixture
def server_conn():
    from transvenous_pacing_gui import server

    return server.Server(port=25565)

# Tests that the server does not initialise to None
def test_server_init(server_conn):
    assert not server_conn == None

# Tests that the server stops with an exception when not connected to a client
def test_server_stop(server_conn):
    with pytest.raises(Exception):
        server_conn.stop()

# Tests that the client does not initialise to None
def test_client_init(client_conn):
    assert not client_conn == None

# Tests that the client starts without exception
def test_client_start(client_conn):
    assert client_conn.start() == None

# Tests that the socket server can be started, then stopped
# Note: a failed test will timeout due to thread blocking on the GIL
def test_server_start_stop(server_conn):
    socket_queue = Queue()

    assert server_conn.start(socket_queue).isAlive() == True

    server_conn.stop()

# Tests that the client can send a packet of data without exception
def test_client_send_data(client_conn):
    assert client_conn.send_data("Hello?") == False

# Tests that the client is able to stop successfully
def test_client_stop(client_conn):
    assert client_conn.stop() == True
