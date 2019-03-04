from guiclient import client
from guiserver import server

import pytest

from queue import Queue

def test_server_init():
    test_server = server.Server(port=911)

    assert not test_server == None

def test_server_stop():
    test_server = server.Server(port=911)

    with pytest.raises(Exception):
        test_server.stop()

def test_client_init():
    test_client = client.Client(port=911)

    assert not test_client == None

def test_client_start():
    test_client = client.Client(port=911)

    assert test_client.start() == None

def test_client_send_data():
    test_client = client.Client(port=911)

    assert test_client.send_data("Hello?") == False

def test_client_stop():
    test_client = client.Client(port=911)

    with pytest.raises(Exception):
        test_client.stop()