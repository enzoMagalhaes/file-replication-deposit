import socket

class FileClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def deposit(self, file_name, replication_level):
        data = open(file_name,'r').read()
        response_data = f"DEPOSIT:{file_name}:{data}"

        self.client_socket.send(response_data.encode())
        print(self.client_socket.recv(1024).decode())
        self.client_socket.close()


    def retrieve(self, file_name):
        response_data = f"RETRIEVE:{file_name}"

        self.client_socket.send(response_data.encode())
        print(self.client_socket.recv(1024).decode())
        self.client_socket.close()


if __name__ == "__main__":

    client = FileClient("localhost", 8000)
    client.deposit("sample.txt",3)
    # client.send_request("DEPOSIT:sample.txt:3")  # Exemplo de depósito de arquivo com 3 réplicas
    # client.send_request("RETRIEVE:sample.txt")  # Exemplo de recuperação de arquivo
