import socket


class FileClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        return client_socket

    def deposit(self, file_name, replication_level):
        with open(file_name, "r") as file:
            data = file.read()

        response_data = f"DEPOSIT:{file_name}:{replication_level}:{data}"

        sock = self.get_socket()
        sock.send(response_data.encode())
        print(sock.recv(1024).decode())
        sock.close()

    def retrieve(self, file_name):
        response_data = f"RETRIEVE:{file_name}"
        sock = self.get_socket()

        sock.send(response_data.encode())
        data = sock.recv(1024).decode()
        sock.close()

        with open(f"./{file_name}", "w") as file:
            file.write(data)

    def change_replication(self, file_name, new_replication_level):
        response_data = f"CHANGE_REPLICATION:{file_name}:{new_replication_level}"
        sock = self.get_socket()

        sock.send(response_data.encode())
        print(sock.recv(1024).decode())
        sock.close()