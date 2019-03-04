from guiclient import client
from guiserver import server

from queue import Queue

def test_server_init():
    test_server = server.Server(port=911)

    assert not test_server == None

def test_client_init():
    test_client = client.Client(port=911)

    assert not test_client == None
