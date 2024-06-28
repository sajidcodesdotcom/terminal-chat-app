import socket
import threading

# list to keep track of connected clients
clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast_message(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except Exception as e:
            raise e
    client_socket.close()

def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode('utf-8'))


def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "0.0.0.0"
    port = 8000
    server.bind((server_ip, port))
    server.listen(10) # listen for 10 connections (more than 10 clients are not allowed to connect simultaneously.
    print(f"listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}\n") 

    threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
