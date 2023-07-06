import socket
import threading

class FileServer:
    SIZE = 1024

    def __init__(self, host, port,replication_ports):
        self.host = host
        self.port = port
        self.replication_ports = replication_ports
        self.file_replication = {}

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
            response = self.deposit(file_name, int(replication_level), data)

        elif command == "RETRIEVE":
            _, file_name = request_args
            response = self.retrieve(file_name=file_name)

        elif command == "CHANGE_REPLICATION":
            _,file_name, new_replication_level = request_args
            response = self.change_replication(file_name=file_name,new_replication_level=int(new_replication_level))

        else:
            response = "Comando inválido."

        client_socket.send(response.encode())
        client_socket.close()

    def deposit(self, file_name, replication_level, data):
        replication_len = len(self.replication_ports)
        if replication_len < replication_level:
            return f"Nivel de replicacao nao suportado, numero de replicas de armazenamento: {replication_len}."

        replication_count = 0
        for i in range(replication_level):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.replication_ports[i]))
            sock.send(f"DEPOSIT:{file_name}:{data}".encode())

            if sock.recv(self.SIZE).decode() == "1":
                replication_count += 1

            sock.close()

        self.file_replication[file_name] = replication_level
        if replication_count == replication_level:
            print(f"Replicacao para {replication_level} nodes concluida com sucesso.")
        else:
            print(
                f"Replicacao para {replication_level} nodes falhou! nivel de replicacao: {replication_count}"
            )

        return "Depósito concluído com sucesso."

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


    def change_replication(self,file_name,new_replication_level):
        file_replication = self.file_replication[file_name]
        if file_replication > new_replication_level:
            for i in range(file_replication-new_replication_level):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(
                        (self.host, self.replication_ports[(file_replication-1)-i])
                    )
                    sock.send(f"DELETE:{file_name}".encode())
                    sock.close()
        elif file_replication < new_replication_level:
            data = self.retrieve(file_name)
            self.deposit(file_name=file_name,replication_level=new_replication_level,data=data)


        message = f"nivel de replicacao do arquivo {file_name} modificado para {new_replication_level}"
        print(message)

        return message


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 3000
    REPLICATION_PORTS = [5000,5001,5002,5003,5004]

    server = FileServer(HOST,PORT,REPLICATION_PORTS)
    server.start()