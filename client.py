import socket
import threading

def receive_message(client_socket, user_id):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                print("Connection closed by the server")
                break
            sender_id, message = response.split(": ", 1)
            if sender_id == user_id:
                print(f"ME: {message}")
            else:
                print(f"{sender_id}: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

def send_message(client_socket, user_id):
    while True:
        try:
            message = input()
            if message.strip().lower() == "exit":
                client_socket.close()
                break
            message = f"\n -> {message}"
            client_socket.send(f"{user_id}: {message}".encode('utf-8'))
        except Exception as e:
            raise e
            

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    client_socket.connect((server_ip, server_port))
    print("-------connected to the server----------\n")
    print("-------Welcome to terminal chatting---------\n")
    user_id = input("To begin the chatting, please assign yourself any name: ")
    print('------happy chatting, to exit the chat simply send the word "exit" or ctrl+c"--------\n')

    threading.Thread(target=receive_message, args=(client_socket, user_id)).start()
    threading.Thread(target=send_message, args=(client_socket, user_id)).start()



if __name__ == "__main__":
    start_client()
