"""
.. module:: server
    :platform: Windows
    :synopsis: Multithreaeded TCP/IP socket server to avoid hanging the GUI
 
.. moduleauthor:: Nam Tran <tranngocnam97@gmail.com>
"""

# Standard Library imports
import socket
import threading
from queue import Queue

class Server:
    """Multithreaeded TCP/IP socket server to avoid hanging the GUI
 
    This class provides basic functionality to connect to its partner TCP/IP
    socket client.
    """

    def __init__(self, port, host=socket.gethostname()):
        """Constructor
 
        Args:
            port (int): Network port for the socket connection.
            host (str, optional): Hostname for the server to use. Defaults to localhost.
        """
        self.host = host
        self.port = port

    def start(self, queue):
        """Starts a socket server listener in a new thread.

        Args:
            queue (queue): Mutex for the server thread
 
        Returns:
            Server thread handle.
        """
        print("Starting Server Socket")

        # Initialises the socket server
        self.server = socket.socket()
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        # Sets up and starts the server thread
        self.server_thread = threading.Thread(target=self.listen, args=(queue,))
        self.server_thread.start()

        # Returns the server thread
        return self.server_thread

    def stop(self):
        """Stops the client-server connection. It also closes the open threads.
        """
        print("Closing connection with client...")
        self.stop_accept()
        self.server_thread.join()
        self.connection.close()

    def receive_data(self, connection, address, queue):
        """Blocking wait for a message

        Args:
            connection: socket connection to read from
            address: localhost address
            queue: mutex to output read message to
        """
        message = connection.recv(1024)

        queue.put(message)
        
        return message

    def set_hostname(self, host):
        """Sets the target hostname
 
        Args:
            host (str): Hostname to connect to.
        """
        self.host = host

    def get_hostname(self):
        """Gets the target hostname
 
        Returns:
            hostname of the target server
        """
        return self.host

    def listen(self, queue):
        """Creates an active listener loop for incoming data

        Args:
            queue: mutex to output read message to
        """
        (self.connection, self.address) = self.server.accept()
        print("Connection established with client...")

        # Infinite loop that needs to be broken with a close command
        while True:
            # Receive data from the receive data thread
            message = self.receive_data(self.connection, self.address, queue)

            if message == b'close':
                break

    def stop_accept(self):
        """Opens a new socket client to force close a socket server if it is hanging."""

        # Try to open the tempory client and close the socket
        try:
            with socket.socket() as tmp_client:
                # Connect to the server
                tmp_client.connect((self.host, self.port))
                stop_message = "close"
                # Send the close command
                tmp_client.send(stop_message.encode())
                print("Forcing server closed")
        # Print any exceptions
        except Exception as e:
            print(e)

# Code to run if the script is called by itself
if __name__ == '__main__':
    # Mutex
    queue = Queue()

    # Server instantiation
    test_server = Server(port=911)
    test_server.start(queue)

    # Message to be
    message = ''

    # Infinite loop to be broken out of
    while True:
        # If the queue is not empty
        if not queue.empty():
            # Get value from the queue
            message = queue.get()
            print(message)

            # Break out of the loop if the close command is found
            if message == b'close':
                break

    # Close out of all server connection stuff
    test_server.stop()
