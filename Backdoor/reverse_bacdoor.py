import socket

connection = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

connection.connect(('172.25.248.236', 4444))
connection.send(b'Hello, Server! \n')
received_data = connection.recv(1024)
print(f'Received: {received_data}')

connection.close()