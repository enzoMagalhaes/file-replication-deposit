import os
import socket
import threading

class ReplicationDeposit:
    SIZE = 1024

    def __init__(self, host,port) -> None:
        self.host = host
        self.port = port
        self.files_folder = f"./replication"
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def deposit(self, file_name, data) -> bool:
        try:
            open(f"{self.files_folder}/{file_name}", "w").write(data)
            return "1"
        except:
            return "0"

    def retrieve(self, file_name) -> str:
        try:
            return open(f"{self.files_folder}/{file_name}", "r").read()
        except:
            return "-1"

    def delete(self, file_name) -> str:
        file_path = f"{self.files_folder}/{file_name}"
        if os.path.isfile(file_path):
            os.remove(file_path)
            return "1"
        else:
            return "0"

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        while True:
            file_server_socket, _ = server_socket.accept()
            threading.Thread(
                target=self.handle_request, args=(file_server_socket,)
            ).start()

    def handle_request(self, file_server_socket):
        request = file_server_socket.recv(self.SIZE).decode()
        request_args = request.split(":")
        command = request_args[0]

        if command == "DEPOSIT":
            _, file_name, data = request_args
            response = self.deposit(file_name=file_name, data=data)

        elif command == "RETRIEVE":
            _, file_name = request_args
            response = self.retrieve(file_name=file_name)

        elif command == "DELETE":
            _, file_name = request_args
            response = self.delete(file_name=file_name)

        else:
            response = "Comando inválido."

        file_server_socket.send(response.encode())
        file_server_socket.close()


if __name__ == "__main__":
    PORT = 5000
    ReplicationDeposit("0.0.0.0",5000).start()
