import os
import socket
import threading

class ReplicationDeposit:
    SIZE = 1024

    def __init__(self,host,port) -> None:
        self.host = host
        self.port = port
        self.files_folder = f'./replication_{port}'
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def deposit(self,file_name,data) -> bool:
        try:
            open(f"{self.files_folder}/{file_name}", "w").write(data)
            return "1"
        except:
            return "0"

    def check_file(self,file_name) -> str:
        return os.path.exists(f"{self.files_folder}/{file_name}")
    
    def retrieve(self,file_name) -> str:
        try:
            return open(f"{self.files_folder}/{file_name}", "r").read()
        except:
            return "-1"
        
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        while True:
            file_server_socket, address = server_socket.accept()
            # print(f"replication_{self.port} Conexão estabelecida com {address[0]}:{address[1]}")
            threading.Thread(target=self.handle_request, args=(file_server_socket,)).start()

    def handle_request(self, file_server_socket):
        request = file_server_socket.recv(self.SIZE).decode()
        request_args = request.split(":")
        command = request_args[0]

        if command == "DEPOSIT":
            _, file_name, data = request_args
            response = self.deposit(file_name=file_name,data=data)

        elif command == "RETRIEVE":
            _, file_name = request_args
            response = self.retrieve(file_name=file_name)

        else:
            response = "Comando inválido."

        file_server_socket.send(response.encode())
        file_server_socket.close()

