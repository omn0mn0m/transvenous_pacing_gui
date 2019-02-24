import socket

server = socket.socket()
host = socket.gethostname()
port = 911

server.bind((host, port))
server.listen(5)

message = ''
(connection, address) = server.accept()
print("Connection established with client...")

while not message == 'close':
    message = input("Enter a message to send: ").lower()
    
    connection.send(message.encode())

connection.close()
