#!/usr/bin/python3

import random
import time
import socket
from threading import Thread
from grid import *

def handle_client(client_socket, player, grids, turn, other_socket, scores):
    # une demande pour savoir c'est qui veut jouer le joueur ou le bot
    client_socket.send("Do you want to play yourself or let a bot play? (type 'me' or 'bot'): ".encode())
    player_choice = client_socket.recv(1024).decode().strip().lower()
    
    is_bot = (player_choice == 'bot')
    print(f"Player {player} chose to play {'bot' if is_bot else 'me'}")

    while True:
        client_socket.send(f"Welcome Player {player}\n".encode())
        client_socket.send(grids[player].display_string().encode())

        while grids[0].gameOver() == -1:
            if turn[0] == player:
                client_socket.send("Your turn!\n".encode())
                
                if is_bot:
                    # pour que le bot joue les coups aleatoire dans des cases vides
                    shot = random.choice([i for i, cell in enumerate(grids[0].cells) if cell == EMPTY])
                    client_socket.send(f"Bot played move {shot}\n".encode())
                else:
                    shot = -1
                    while shot < 0 or shot >= NB_CELLS:
                        client_socket.send(f"Player {player}, enter your move (0-8): ".encode())
                        shot = int(client_socket.recv(1024).decode().strip())
                # si la case est deja prises coup perdu
                if grids[0].cells[shot] != EMPTY:
                    client_socket.send("Cell already taken.\n".encode())
                    grids[player].cells[shot] = grids[0].cells[shot]
                # si case vide alors coup joué
                else:
                    grids[player].cells[shot] = player
                    grids[0].play(player, shot)
              
                turn[0] = J2 if player == J1 else J1
            else:
                client_socket.send("Waiting for the other player...\n".encode())

            while turn[0] != player:
                time.sleep(1)

            client_socket.send(grids[player].display_string().encode())    

        # quand le jeu est terminé 
        client_socket.send("Game over\n".encode())
        client_socket.send(grids[0].display_string().encode())
        other_socket.send("Game over\n".encode())
        other_socket.send(grids[0].display_string().encode())

        # envoie du mssg du resultat à chaque joueur
        if grids[0].gameOver() == player:
            client_socket.send("You have won!\n".encode())
            other_socket.send("You have lost!\n".encode())
            
            scores[player - 1] += 1 #Ajoute d'un point au joueur gagnant 

        elif grids[0].gameOver() == (J2 if player == J1 else J1):
            client_socket.send("You have lost!\n".encode())
            other_socket.send("You have won!\n".encode())
            scores[(J2 if player == J1 else J1) - 1] += 1
        else:
            client_socket.send("It's a draw!\n".encode())
            other_socket.send("It's a draw!\n".encode())

        # affichage du score 
        client_socket.send(f"Current Score - Player 1: {scores[0]}, Player 2: {scores[1]}\n".encode())
        other_socket.send(f"Current Score - Player 1: {scores[0]}, Player 2: {scores[1]}\n".encode())

        # Demande si les joueurs veulent jouer une autre partie
        client_socket.send("Do you want to play again? (yes/no): ".encode())
        other_socket.send("Do you want to play again? (yes/no): ".encode())
        response = client_socket.recv(1024).decode().strip().lower()
        other_response = other_socket.recv(1024).decode().strip().lower()

        if response != "yes" or other_response != "yes":
            client_socket.send("Thanks for playing!\n".encode())
            other_socket.send("Thanks for playing!\n".encode())
            break  # Fin de la boucle de jeu

        # Réinitialise la grille pour une nouvelle partie
        grids[0] = grid()
        grids[player] = grid()
        grids[J2 if player == J1 else J1] = grid()


    client_socket.close()
    other_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(2)
    print("Server listening on port 5555")

    grids = [grid(), grid(), grid()]
    turn = [J1]
    scores = [0, 0]  # Initialisation des scores pour chaque joueur

    # Acceptation des connexions et gestion des deux joueurs
    client_socket1, _ = server_socket.accept()
    print("Connection from player 1")
    client_socket2, _ = server_socket.accept()
    print("Connection from player 2")

    # Création des threads pour chaque joueur
    Thread(target=handle_client, args=(client_socket1, J1, grids, turn, client_socket2, scores)).start()
    Thread(target=handle_client, args=(client_socket2, J2, grids, turn, client_socket1, scores)).start()

if __name__ == "__main__":
    main()

