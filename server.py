import socket
import concurrent.futures

# list to keep track of connected clients
clients = []


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                print(
                    "\n === Received an empty message, the client might have disconnected === \n"
                )
                break
            broadcast_message(message, client_socket)
        except Exception as e:
            print(f"\n Error handling client's message: {e} \n")
            break  # Exit the loop if there is an error
    remove_client(client_socket)


def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                remove_client(client)


def broadcast_client_count():
    client_count_message = f"Total connected users ATM: {len(clients)} \n"
    for client in clients:
        try:
            client.send(client_count_message.encode("utf-8"))
        except Exception as e:
            print(f"Error broadcasting client count: {e}")
            remove_client(client)


def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()
        print(f"Client disconnected. Total clients: {len(clients)} \n")
        broadcast_client_count()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "0.0.0.0"
    port = 8000
    server.bind((server_ip, port))
    server.listen(10)  # listen for 10 connections
    print(f"Listening on {server_ip}:{port}")

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    try:
        while True:
            client_socket, client_address = server.accept()
            clients.append(client_socket)
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            print(f"Total connected users: {len(clients)}")
            broadcast_client_count()
            executor.submit(handle_client, client_socket)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        for client in clients:
            client.close()
        server.close()
        executor.shutdown(wait=True)


if __name__ == "__main__":
    start_server()
