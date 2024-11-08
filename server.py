from grid import grid
import socket
import threading

def handle_client(client_socket, player, game):
    # Fonction pour gérer les interactions avec chaque joueur
    while game.gameOver() == -1:
        move = int(client_socket.recv(1024).decode("utf-8"))  # Recevoir le coup
        if game.is_valid_move(move, player):
            game.play_move(move, player)
            # Envoyer l'état du jeu après le coup
            client_socket.send(game.get_state().encode("utf-8"))
        else:
            # Informer le joueur que son coup est invalide
            client_socket.send("Coup invalide, essayez encore".encode("utf-8"))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5555))  # Adresse et port
    server.listen(2)
    
    game = grid()  # Un objet qui gère l'état du jeu
    
    print("En attente de connexions...")
    
    # Accepter les connexions des deux joueurs
    player1, addr1 = server.accept()
    print(f"Joueur 1 connecté depuis {addr1}")
    player2, addr2 = server.accept()
    print(f"Joueur 2 connecté depuis {addr2}")
    
    # Créer des threads pour gérer les joueurs
    threading.Thread(target=handle_client, args=(player1, 1, game)).start()
    threading.Thread(target=handle_client, args=(player2, 2, game)).start()

start_server()
