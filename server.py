import socket
import concurrent.futures

# list to keep track of connected clients
clients = []


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message == "exit":
                broadcast_message(message, client_socket, has_left=True)
                remove_client(client_socket)
                break
            if message:
                broadcast_message(message, client_socket, has_left=False)
            else:
                print("Somthing went wrong while broadcasting the message")
                break
        except Exception as e:
            raise e


def broadcast_message(message, client_socket, has_left):
    for client in clients:
        if client != client_socket:
            client.send(message.encode("utf-8"))
        if has_left and client == client_socket: 
            client.send(message.encode('utf-8'))



def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "0.0.0.0"
    port = 8000
    server.bind((server_ip, port))
    server.listen(
        10
    )  # listen for 10 connections (more than 10 clients are not allowed to connect simultaneously.
    print(f"listening on {server_ip}:{port}")

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    while True:
        try:
            client_socket, client_address = server.accept()
            clients.append(client_socket)
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            executor.submit(handle_client, client_socket)
        except KeyboardInterrupt:
            print("\n Shutting down server...")
            for client in clients:
                client.close()
            server.close()
            break


if __name__ == "__main__":
    start_server()
