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

        # Si c'est au tour du joueur, on attend l'entrée du joueur
        if "enter your move" in response:
            move = input()
            client_socket.send(move.encode())

    client_socket.close()

if __name__ == "__main__":
    main('localhost')


