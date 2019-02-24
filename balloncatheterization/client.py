import socket

client = socket.socket()
host = socket.gethostname()
port = 911

client.connect((host, port))

message = ''

while not message == 'close':
    message = client.recv(1024)
    print(message)

client.close()
