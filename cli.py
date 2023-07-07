import argparse
from client.client import FileClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="client CLI do sistema de depósito de arquivos")

    parser.add_argument("--host", default="0.0.0.0", help="Server host address")
    parser.add_argument("--port", type=int, default=3000, help="Server port number")

    args = parser.parse_args()

    client = FileClient(args.host, args.port)

    while True:
        request = input("> ")
        if request == "quit":
            break
        elif request == "help":
            print(
                "Enter a request (DEPOSIT myfile.txt <replication_level>, RETRIEVE myfile.txt, CHANGE_REPLICATION myfile.txt <new_replication_level>) or 'quit' to exit: "
            )

        parts = request.split()
        command = parts[0]

        if command == "DEPOSIT":
            if len(parts) != 3:
                print(
                    "Invalid request format. Usage: DEPOSIT myfile.txt <replication_level>"
                )
                continue

            file_name = parts[1]
            replication_level = int(parts[2])
            client.deposit(file_name, replication_level)
        elif command == "RETRIEVE":
            if len(parts) != 2:
                print("Invalid request format. Usage: RETRIEVE myfile.txt")
                continue

            file_name = parts[1]
            client.retrieve(file_name)
        elif command == "CHANGE_REPLICATION":
            if len(parts) != 3:
                print(
                    "Invalid request format. Usage: CHANGE_REPLICATION myfile.txt <new_replication_level>"
                )
                continue

            file_name = parts[1]
            new_replication_level = int(parts[2])
            client.change_replication(file_name, new_replication_level)
        else:
            print("Invalid command. Please try again.")
