import socket
import multiprocessing

class Server:

    def __init__(self, port, host=socket.gethostname()):
        self.host = host
        self.port = port

    def start(self):
        print("Starting Socket")
        self.server = socket.socket()
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        (self.connection, self.address) = self.server.accept()
        print("Connection established with client...")

    def stop(self):
        self.connection.close()

    def receive_data(self):
        message = self.server.recv(1024)
        
        return message
        

if __name__ == '__main__':
    test_server = Server(port=911)
    test_server.start()

    message = ''

    while not message == 'close':
        
        test_server.receive_data()
