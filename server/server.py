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

    def criar_sockets(self, n_copies):
       for i in range(len(self.sockets),int(n_copies)):
          port = 8001 + i
          newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          newSocket.bind(('localhost', port))
          newSocket.listen(5)
          self.sockets[port] = newSocket
          print("New port: {}:{}".format('localhost', port))

    # Socket replica aceita requisições do server_socket
    def abrir_deposito(self, socket, porta):
      origin, address = socket.accept()
      request = origin.recv(self.SIZE).decode()
      request_args = request.split(":")

      print(f"Conexão estabelecida com {address[0]}:{address[1]}")
      _, file_name, data = request_args
      with open(f"replicas/{porta}/{file_name}", "w") as file:
         file.write(data)

      socket.send(f"Armazenado na porta {porta}".encode())
      socket.shutdown(socket.SHUT.RDWR)
      socket.close()

    def depositar(self, request):
      # Implementar a lógica de replicação adequada para armazenar o arquivo em diferentes locais 
      request_args = request.split(":")
      _, file_name, data, n_copies = request_args

      # Checa quantidade de aplicações disponíveis
      if int(n_copies) > len(self.sockets):
        self.criar_sockets(n_copies)
      
      for i in range(8001, 8001+int(n_copies)):
        threading.Thread(target=self.abrir_deposito, name=f"Thread:{i}", args=(self.sockets[i], i,)).start()
        self.server_socket.connect((self.host,i))
        self.server_socket.sendall(f"DADOS:{file_name}:{data}:{n_copies}".encode())
        self.server_socket.shutdown(socket.SHUT_RDWR)
        time.sleep(0.1)
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
          if self.depositar(request):
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