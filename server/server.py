import socket
import threading
from ReplicationDeposit import ReplicationDeposit


class FileServer:
    SIZE = 1024

    def __init__(self, host):
        self.last_replication_port = 3000
        self.host = host
        self.port = self.get_available_port()
        self.max_replication = 0
        self.replication_ports = []

    def get_available_port(self):
        available_port = None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try: 
                sock.bind((self.host, self.last_replication_port))
            except:
                # Conexao falhou, porta disponivel
                print(f"porta disponivel: {self.last_replication_port}")
                available_port = self.last_replication_port
            finally:
                sock.close()
                self.last_replication_port += 1
                if available_port:
                    return available_port

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
            _, file_name, replication_level, data = request_args

            # try:
            self.deposit(file_name, int(replication_level), data)
            response = "Depósito concluído com sucesso."
            # except Exception as e:
            # response = f"Ocorreu um erro no deposito. erro: {e}"

        elif command == "RETRIEVE":
            _, file_name = request_args
            response = self.retrieve(file_name=file_name)

        else:
            response = "Comando inválido."

        client_socket.send(response.encode())
        client_socket.close()

    def deposit(self, file_name, replication_level, data):
        if self.max_replication < replication_level:
            for i in range(replication_level - self.max_replication):
                replication_port = self.get_available_port()

                threading.Thread(
                    target=ReplicationDeposit(self.host, replication_port).start,
                    args=(),
                ).start()

                self.replication_ports.append(replication_port)

            self.max_replication = replication_level

        replication_count = 0
        for i in range(replication_level):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.replication_ports[i]))
            sock.send(f"DEPOSIT:{file_name}:{data}".encode())

            if sock.recv(self.SIZE).decode() == "1":
                replication_count += 1

            sock.close()

        if replication_count == replication_level:
            print(f"Replicacao para {replication_level} nodes concluida com sucesso.")
        else:
            print(
                f"Replicacao para {replication_level} nodes falhou! nivel de replicacao: {replication_count}"
            )

    def retrieve(self, file_name):
        for i in range(len(self.replication_ports)):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(
                    (self.host, self.replication_ports[i])
                )
                sock.send(f"RETRIEVE:{file_name}".encode())

                data = sock.recv(self.SIZE).decode()
                sock.close()

                if(data != "-1"):
                    return data
        return "Arquivo nao encontrado."


if __name__ == "__main__":
    HOST = "0.0.0.0"

    server = FileServer(HOST)
    server.start()
