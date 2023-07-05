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
           self.sockets.append(8001+i)

      data = open(file_name,'r').read()
      response_data = f"DEPOSIT:{file_name}:{data}:{n_copies}"

      self.client_socket.send(response_data.encode())
      self.client_socket.shutdown(socket.SHUT_RDWR)
      self.client_socket.accept()
      print(self.client_socket.recv(1024).decode())
      self.client_socket.close()

    def retrieve(self, file_name):
      response_data = f"RETRIEVE:{file_name}"

      self.client_socket.sendall(response_data.encode())

      with open(file_name, "wb") as file:
        while True:
          chunk = self.client_socket.recv(4096)
          if not chunk:
            break
          file.write(chunk)

      print('\nArquivo recebido com sucesso.')

      time.sleep(0.1)  # Add a small delay (e.g., 100 milliseconds)
      self.client_socket.shutdown(socket.SHUT_RDWR)
      self.client_socket.close()


if __name__ == "__main__":
    client = FileClient("localhost", 8000)
    client.deposit("teste.txt", 2)
    #client.retrieve("teste.txt")
    client.close()
