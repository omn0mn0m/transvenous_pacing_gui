"""
.. module:: client
    :platform: Windows
    :synopsis: Multithreaeded TCP/IP socket client to avoid hanging the GUI
 
.. moduleauthor:: Nam Tran <tranngocnam97@gmail.com>
"""

# Standard Library imports
import socket

class Client:
    """Multithreaeded TCP/IP socket client to avoid hanging the GUI
 
    This class provides basic functionality to connect to its partner TCP/IP
    socket server.
    """

    def __init__(self, port, host=socket.gethostname()):
        """Constructor
 
        Args:
            port (int): Network port for the socket connection.
            host (str, optional): Hostname to connect to. Defaults to localhost.
        """
        self.host = host
        self.port = port
        self.client = socket.socket()

    def start(self):
        """Starts the client-server connection
 
        Returns:
            None if unable to connect.
        """
        print("Starting Client Socket")
        
        try:
            self.client.connect((self.host, self.port))
        except:
            print("Unable to connect...")

            return None

    def stop(self):
        """Stops the client-server connection. It also will send a close command
        to the socket server to close.
 
        Returns:
            True if successful.
        """
        stop_message = 'close'

        # Tries to send the kill signal to the server, closing itself as well
        try:
            self.client.send(stop_message.encode())
            print("Closing connection with server...")
        # Prints out any errors encountered
        except Exception as e:
            print(e)

        return True

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

    def get_ip(self):
        """Gets the client IP address
 
        Returns:
            IP address of the client
        """
        return socket.gethostbyname(self.host)

    def send_data(self, message):
        """Sends a message to the socket server
 
        Args:
            message (str): message to send to the server

        Returns:
            False if unable to send the message
        """
        # Try to send the message
        try:
            self.client.send(message.encode())
        # Prints an error if unable to send
        except:
            print("Unable to send a message...")

            return False

# Code to run if the script is called by itself
if __name__ == '__main__':
    # Initialise the client and start it
    test_client = Client(port=911)
    test_client.start()

    message = ''

    # Infinite loop to break out when the close signal is sent
    while True:
        # User input
        message = input("Enter a message to send: ").lower()

        # Sends the message to the socket server
        test_client.send_data(message)
        
        # Stops the server and client if the kill message is sent
        if message == 'close':
            test_client.stop()
            break
