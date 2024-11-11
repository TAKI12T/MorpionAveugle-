#!/usr/bin/python3

import time 
import socket
from threading import Thread
from grid import *

def handle_client(client_socket, player, grids, turn, other_socket):
    client_socket.send(f"Welcome Player {player}\n".encode())
    client_socket.send(grids[player].display_string().encode())

    while grids[0].gameOver() == -1:
        if turn[0] == player:
            # C'est au tour de ce joueur de jouer
            client_socket.send("Your turn!\n".encode())
            shot = -1
            while shot < 0 or shot >= NB_CELLS or grids[0].cells[shot] != EMPTY:
                client_socket.send(f"Player {player}, enter your move (0-8): ".encode())
                shot = int(client_socket.recv(1024).decode().strip())
                if grids[0].cells[shot] != EMPTY:
                    client_socket.send("Cell already taken, try again.\n".encode())
            
            # mise a jour de la grille commune et du joueur           
            grids[0].play(player, shot)
            grids[player].cells[shot] = grids[0].cells[shot]
            
            # change de tour
            turn[0] = J2 if player == J1 else J1
        else:
            client_socket.send("Waiting for the other player...\n".encode())
        while turn[0] != player:
            time.sleep(1) 

        # Envoie uniquement la partie de la grille pour le joueur courant
        client_socket.send(grids[player].display_string().encode())

    # Quand le jeu est terminé
    client_socket.send("Game over\n".encode())
    client_socket.send(grids[0].display_string().encode())
    other_socket.send("Game over\n".encode())
    other_socket.send(grids[0].display_string().encode())

    # envoie  msg du resultat à chaque joueur
    if grids[0].gameOver() == player:
        client_socket.send("You have won!\n".encode())
        other_socket.send("You have lost!\n".encode())
    elif grids[0].gameOver() == (J2 if player == J1 else J1):
        client_socket.send("You have lost!\n".encode())
        other_socket.send("You have won!\n".encode())
    else:
        client_socket.send("It's a draw!\n".encode())
        other_socket.send("It's a draw!\n".encode())

    client_socket.close()
    other_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(2)
    print("Server listening on port 5555")

    grids = [grid(), grid(), grid()]
    turn = [J1]  

    # Acceptation des connexions et gestion des deux joueurs
    client_socket1, _ = server_socket.accept()
    print("Connection from player 1")
    client_socket2, _ = server_socket.accept()
    print("Connection from player 2")

    # Création des threads pour chaque joueur
    Thread(target=handle_client, args=(client_socket1, J1, grids, turn, client_socket2)).start()
    Thread(target=handle_client, args=(client_socket2, J2, grids, turn, client_socket1)).start()

if __name__ == "__main__":
    main()

