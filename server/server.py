import socket
import threading
import time

class FileServer:
    SIZE = 1024

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockets = {}
        self.files = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Conexão estabelecida com {address[0]}:{address[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def criar_sockets(self, porta):
      newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      newSocket.bind(('localhost', int(porta)))
      newSocket.listen(5)
      self.sockets[porta] = newSocket
      print(f"New port: {'localhost'}:{porta}")

      t = threading.Thread(target=self.run_sockets, args=(newSocket,porta))
      t.daemon = True
      t.start()

    # Thread de cada socket (replica) rodando
    def run_sockets_deposit(self, socket, port):
      while True:
        print(f"Esperando conexão na porta {port}")
        origin, address = socket.accept()
        print(f"Conexão estabelecida com {address[0]}:{address[1]} na porta {port}")

        request = origin.recv(self.SIZE).decode()
        request_args = request.split(":")
        _, file_name, data = request_args

        with open(f"replicas/{port}/{file_name}", "w") as file:
          file.write(data)
      
        origin.send("Arquivo armazenado com sucesso".encode())
        origin.close()

    def depositar(self, request):
      # Implementar a lógica de replicação adequada para armazenar o arquivo em diferentes locais 
      request_args = request.split(":")
      _, file_name, data, porta = request_args

      # Checa quantidade de aplicações disponíveis
      if porta not in self.sockets:
        self.criar_sockets(porta)

      return True

    def handle_client(self, client_socket):
        request = client_socket.recv(self.SIZE).decode()
        request_args = request.split(":")
        command = request_args[0]
        time.sleep(0.2)

        if command == "DEPOSIT":
          if self.depositar(request):
            response = "Deposito realizado com sucesso"
          else:
             response = "Nao foi possivel realizar o deposito"

        #elif command == "RETRIEVE":
        #  if self.retornar(request_args):
        #    response = "Arquivo retornado com sucesso"
        #  else:
        #     response = "Nao foi possivel encontrar arquivo solicitado"
        
        else:
            response = "Comando inválido."

        client_socket.send(response.encode())
        client_socket.close()
        

if __name__ == "__main__":
    # Execução do servidor
    server = FileServer("localhost", 8000)
    server.start()