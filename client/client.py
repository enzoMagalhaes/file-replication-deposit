import socket
import time

class FileClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockets = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def deposit(self, file_name, n_copies):
      if n_copies > len(self.sockets):
        for i in range(len(self.sockets),n_copies):
          port = 8001+i
          self.sockets.append(port)

          data = open(file_name,'r').read()
          response_data = f"DEPOSIT:{file_name}:{data}:{port}"

          self.client_socket.send(response_data.encode())
          self.client_socket.close()
          self.client_socket.connect((self.host, self.port))
          print(self.client_socket.recv(1024).decode())
          self.client_socket.close()
      

if __name__ == "__main__":
    client = FileClient("localhost", 8000)
    client.deposit("teste.txt", 2)
    #client.retrieve("teste.txt")
    client.close()
