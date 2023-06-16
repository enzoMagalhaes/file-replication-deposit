import socket
import threading


class FileServer:
    SIZE = 1024

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            client_socket, address = server_socket.accept()
            print(f"Conexão estabelecida com {address[0]}:{address[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        request = client_socket.recv(self.SIZE).decode()
        request_args = request.split(":")
        command = request_args[0]

        if command == "DEPOSIT":
            # Implementar a lógica de replicação adequada para armazenar o arquivo em diferentes locais
            _, file_name, data = request_args
            open(file_name, "w").write(data)
            response = "Depósito concluído com sucesso."

        elif command == "RETRIEVE":
            # Implementar a lógica de recuperação adequada para encontrar o arquivo replicado e devolver ao cliente
            _, file_name = request_args
            response = open(file_name, "r").read()

        else:
            response = "Comando inválido."

        client_socket.send(response.encode())
        client_socket.close()


if __name__ == "__main__":
    # Execução do servidor
    server = FileServer("localhost", 8000)
    server.start()
