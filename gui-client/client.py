import socket

client = socket.socket()
host = socket.gethostname()
port = 911

client.connect((host, port))

message = ''

while not message == 'close':
   message = input("Enter a message to send: ").lower()
   client.send(message.encode())

client.close()
