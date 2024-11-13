#!/usr/bin/python3

import random
import time
import socket
from threading import Thread
from grid import *

def handle_client(client_socket, player, grids, turn, other_socket, scores, grid_updated, observer_socket=None):
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
                    shot = random.choice([i for i, cell in enumerate(grids[0].cells) if cell == EMPTY])
                    client_socket.send(f"Bot played move {shot}\n".encode())
                else:
                    shot = -1
                    while shot < 0 or shot >= NB_CELLS:
                        client_socket.send(f"Player {player}, enter your move (0-8): ".encode())
                        try:
                            shot = int(client_socket.recv(1024).decode().strip())
                        except:
                            client_socket.send("Error : Type a number within [0-8]\n".encode())
                            shot = -1
                    if grids[0].cells[shot] != EMPTY:
                        grids[player].cells[shot] = grids[0].cells[shot]
                        client_socket.send("Cell already taken, Try Again.\n".encode())
                        client_socket.send(grids[player].display_string().encode())
                        shot = -1

                grids[player].cells[shot] = player
                grids[0].play(player, shot)
                grid_updated[0] = True  #l'indicateur a True pour signaler un changement

                turn[0] = J2 if player == J1 else J1
            else:
                client_socket.send("Waiting for the other player...\n".encode())

            while turn[0] != player:
                time.sleep(1)

            client_socket.send(grids[player].display_string().encode())

        client_socket.send("Game over\n".encode())
        client_socket.send(grids[0].display_string().encode())
        other_socket.send("Game over\n".encode())
        other_socket.send(grids[0].display_string().encode())

        if observer_socket:
            observer_socket.send("Game over\n".encode())
            observer_socket.send(grids[0].display_string().encode())

        if grids[0].gameOver() == player:
            client_socket.send("You have won!\n".encode())
            other_socket.send("You have lost!\n".encode())
            scores[player - 1] += 1
        elif grids[0].gameOver() == (J2 if player == J1 else J1):
            client_socket.send("You have lost!\n".encode())
            other_socket.send("You have won!\n".encode())
            scores[(J2 if player == J1 else J1) - 1] += 1
        else:
            client_socket.send("It's a draw!\n".encode())
            other_socket.send("It's a draw!\n".encode())

        client_socket.send(f"Current Score - Player 1: {scores[0]}, Player 2: {scores[1]}\n".encode())
        other_socket.send(f"Current Score - Player 1: {scores[0]}, Player 2: {scores[1]}\n".encode())
        if observer_socket:
            observer_socket.send(f"Current Score - Player 1: {scores[0]}, Player 2: {scores[1]}\n".encode())

        client_socket.send("Do you want to play again? (yes/no): ".encode())
        other_socket.send("Do you want to play again? (yes/no): ".encode())
        response = client_socket.recv(1024).decode().strip().lower()
        other_response = other_socket.recv(1024).decode().strip().lower()

        if response != "yes" or other_response != "yes":
            client_socket.send("Thanks for playing!\n".encode())
            other_socket.send("Thanks for playing!\n".encode())
            if observer_socket:
                observer_socket.send("Players have ended the game. Thanks for watching!\n".encode())
            break

        grids[0] = grid()
        grids[player] = grid()
        grids[J2 if player == J1 else J1] = grid()

    client_socket.close()
    other_socket.close()
    if observer_socket:
        observer_socket.close()

def handle_observer(observer_socket, grids, grid_updated):
    """Fonction pour envoyer la grille à l'observateur uniquement quand il y a un changement."""
    try:
        observer_socket.send("Connected as observer. You will see all moves.\n".encode())
        while True:
            if grid_updated[0]:  
                observer_socket.send(grids[0].display_string().encode())
                grid_updated[0] = False  
            time.sleep(0.5) 
    except:
        observer_socket.close()
        print("Observer disconnected")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(3)
    print("Server listening on port 5555")

    grids = [grid(), grid(), grid()]
    turn = [J1]
    scores = [0, 0]
    grid_updated = [False]  # on a utilisé pour garder l'état modifiable dans les threads

    client_socket1, _ = server_socket.accept()
    print("Connection from player 1")
    client_socket2, _ = server_socket.accept()
    print("Connection from player 2")

    observer_socket = None
    try:
        observer_socket, _ = server_socket.accept()
        print("Connection from observer")
        Thread(target=handle_observer, args=(observer_socket, grids, grid_updated)).start()
    except:
        print("No observer connected")

    Thread(target=handle_client, args=(client_socket1, J1, grids, turn, client_socket2, scores, grid_updated, observer_socket)).start()
    Thread(target=handle_client, args=(client_socket2, J2, grids, turn, client_socket1, scores, grid_updated, observer_socket)).start()

if __name__ == "__main__":
    main()

