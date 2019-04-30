import pytest

from queue import Queue

@pytest.fixture
def client_conn():
    from transvenous_pacing_gui import client

    return client.Client(port=25565)

@pytest.fixture
def server_conn():
    from transvenous_pacing_gui import server

    return server.Server(port=25565)

def test_server_init(server_conn):
    assert not server_conn == None

def test_server_stop(server_conn):
    with pytest.raises(Exception):
        server_conn.stop()

def test_client_init(client_conn):
    assert not client_conn == None

def test_client_start(client_conn):
    assert client_conn.start() == None

def test_server_start_stop(server_conn):
    socket_queue = Queue()

    assert server_conn.start(socket_queue).isAlive() == True

    server_conn.stop()

def test_client_send_data(client_conn):
    assert client_conn.send_data("Hello?") == False

def test_client_stop(client_conn):
    assert client_conn.stop() == True
