#!/usr/bin/python3

import socket

def main(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5555))
    print("Connected to server")

    while True:
        response = client_socket.recv(1024).decode()
        if not response:
            break
        print(response, end="")  
        
        if "enter your move" in response or "Do you want to play again?" in response or "Do you want to play yourself or let a bot play?" in response:
            user_input = input()  
            client_socket.send(user_input.encode())  # Envoie la réponse au serveur

    client_socket.close()

if __name__ == "__main__":
    main('localhost')

