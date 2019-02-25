import socket

class Client:

    def __init__(self, port, host=socket.gethostname()):
        self.host = host
        self.port = port

    def start(self):
        print("Starting Client Socket")
        self.client = socket.socket()
        self.client.connect((self.host, self.port))

    def stop(self):
        print("Closing connection with server...")

    def send_data(self, message):
        self.client.send(message.encode())

if __name__ == '__main__':
    test_client = Client(port=911)
    test_client.start()

    message = ''

    while True:
        message = input("Enter a message to send: ").lower()

        test_client.send_data(message)
        
        if message == 'close':
            test_client.stop()
