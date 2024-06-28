import socket
import threading

def receive_message(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
        except:
            print("connection lost")
            client_socket.close()
            break

def send_message(client_socket):
    while True:
        try:
            reply = input("ME: ")
            client_socket.send(reply.encode('utf-8'))
        except Exception as e:
            raise e
            

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    client_socket.connect((server_ip, server_port))
    print("-------connected to the server----------\n")

    threading.Thread(target=receive_message, args=(client_socket,)).start()
    threading.Thread(target=send_message, args=(client_socket,)).start()



if __name__ == "__main__":
    start_client()
