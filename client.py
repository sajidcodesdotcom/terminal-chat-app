import socket
import threading
from terminaltexteffects.effects.effect_slide import Slide
from terminaltexteffects.effects.effect_rain import Rain
from terminaltexteffects.effects.effect_decrypt import Decrypt
from terminaltexteffects.effects.effect_beams import Beams
from utils import animate_text

def receive_message(client_socket, user_id):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                print("Connection closed by the server")
                client_socket.close()
                break

            if response.strip() == '':
                client_socket.close()
                break
            if response.startswith("Total connected users ATM:"):
                print(response)
            elif ":" in response:
                sender_id, message = response.split(": ", 1)
                text = (f"{sender_id}:\n {message}")
                if response.endswith("HAS LEFT THE CHAT"):
                    animate_text(Decrypt, text)
                else:
                    animate_text(Rain, text)

        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

def send_message(client_socket, user_id):
    while True:
        try:
            message = input()
            client_socket.send(f"{user_id}: -> {message}".encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            break
    client_socket.close()

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = "127.0.0.1"
        server_port = 8000
        client_socket.connect((server_ip, server_port))

        welcome_text = "-------connected to the server----------\n -------Welcome to terminal chatting---------\n -> happy chatting, to exit the chat \n simply press [ctrl+c]\n"

        text = (welcome_text)
        animate_text(Slide, welcome_text)
        user_id = input("To begin the chatting, please assign yourself any name: ")
        animate_text(Beams, "---- You can start chatting now ------\n")

        receiver_thread = threading.Thread(target=receive_message, args=(client_socket, user_id))
        sender_thread = threading.Thread(target=send_message, args=(client_socket, user_id))
        receiver_thread.start()
        sender_thread.start()

        receiver_thread.join()
        sender_thread.join()
    except KeyboardInterrupt:
        animate_text(Decrypt, "\nYou have left the chat")
        try:
            client_socket.send(f"{user_id}: Has left the chat".encode("utf-8"))
        except:
            pass
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()

