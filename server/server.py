import socket
import threading
import os

class FileServer:
    SIZE = 1024

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockets = {}
        self.files = {}

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            client_socket, address = server_socket.accept()
            print(f"Conexão estabelecida com {address[0]}:{address[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def depositar(self, request_args, client_socket):
      # Implementar a lógica de replicação adequada para armazenar o arquivo em diferentes locais
      _, file_name, n_copies = request_args

      with open(file_name, 'rb') as file:
          data = file.read()

      # Checa quantidade de aplicações disponíveis
      if int(n_copies) > len(self.sockets):
        for i in range(len(self.sockets),int(n_copies)):
          port = 8001 + i
          newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          newSocket.bind(('localhost', port))
          newSocket.listen(5)
          self.sockets[port] = newSocket
          print("New port: {}:{}".format('localhost', port))

      print("\n")
      for i in range(int(n_copies)):
        socket_obj = self.sockets[8001+i]
        self.files[8001+i] = file_name

        client_socket.close()
        print("Liberou conexão com client_socket")

        print(type(socket_obj))       
        print("Tentando conexão do server_socket com localhost:{}".format(8001+i))
        socket_obj.accept()
        print("Conexão aceita para a porta {}".format(8001+i))
        socket_obj.sendall(data)
        print("Dados enviados com sucesso")
        socket_obj.close()

      return True

    def retornar(self, request_args):
      _, file_name = request_args
      for porta in self.files:
        if self.files[porta] == file_name:
          socket_obj = self.sockets[porta]

          with open(file_name, "wb") as file:
            while True:
              data = socket_obj.recv(4096)
              if not data:
                break
              file.write(data)
      return True   

    def handle_client(self, client_socket):
        request = client_socket.recv(self.SIZE).decode()
        request_args = request.split(":")
        command = request_args[0]

        if command == "DEPOSIT":
          if self.depositar(request_args, client_socket):
            response = "Deposito realizado com sucesso"
          else:
             response = "Nao foi possivel realizar o deposito"

        elif command == "RETRIEVE":
          if self.retornar(request_args):
            response = "Arquivo retornado com sucesso"
          else:
             response = "Nao foi possivel encontrar arquivo solicitado"
        
        else:
            response = "Comando inválido."

        client_socket.send(response.encode())
        client_socket.close()
        

if __name__ == "__main__":
    # Execução do servidor
    server = FileServer("localhost", 8000)
    server.start()