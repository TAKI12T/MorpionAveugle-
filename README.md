Projet de Réseau : Jeu du Morpion Aveugle

Description du projet
Ce projet consiste à développer une version en réseau du célèbre jeu du Morpion (ou Tic-Tac-Toe) avec une variante appelée Morpion Aveugle. Dans cette version, les joueurs ne peuvent pas voir les coups joués par leur adversaire, créant ainsi un aspect stratégique supplémentaire. Le but est de jouer à deux joueurs connectés à un serveur, avec des possibilités d'extensions pour améliorer l'expérience de jeu.

1.1 Le Jeu du Morpion
Le Morpion est un jeu à deux joueurs qui se joue sur une grille de 3x3 cases. Chaque joueur joue à son tour en marquant une case avec son symbole (X ou O). Le premier joueur qui parvient à aligner trois de ses symboles sur la grille gagne la partie. Si toutes les cases sont remplies sans qu'un joueur ait gagné, la partie se termine par un match nul.

1.2 Le Morpion Aveugle
Dans la version Aveugle du jeu, chaque joueur ne voit pas les coups de son adversaire. Lorsqu'un joueur tente de jouer sur une case déjà occupée, il est informé que cette case est prise et doit choisir une autre case. Le but du jeu est donc d'essayer de deviner où l'adversaire a joué tout en avançant avec ses propres stratégies.

1.3 Passage en Réseau
Le jeu a été adapté pour permettre à deux joueurs de s'affronter en réseau via un serveur central. Le serveur attend les connexions des joueurs (clients), et une fois la connexion établie, il transmet les informations sur les coups joués et l'état du jeu à chaque client. Un protocole textuel simple a été utilisé pour la communication entre le serveur et les clients, ce qui permet de suivre facilement le déroulement de la partie.

Le projet comprend les fichiers suivants :

grid.py : gestion de la grille de jeu.
main.py : logique du serveur et des clients.
Les joueurs peuvent se connecter à un serveur en indiquant son adresse lors du lancement de l'application. Le serveur gère la communication entre les joueurs et l'état du jeu.

1.4 Extensions
Plusieurs fonctionnalités supplémentaires ont été implémentées ou peuvent être ajoutées :

Support des parties multiples : possibilité de jouer plusieurs parties avec comptage des scores.
Mode robot : un joueur peut être remplacé par un robot qui joue des coups aléatoires.
Mode observateur : un ou plusieurs clients peuvent observer la partie sans y participer.
Reprise de partie après une déconnexion : si la connexion entre un client et le serveur est interrompue, la partie peut être mise en pause jusqu'à la reconnexion du client.
Gestion des pannes de clients : si un client tombe en panne (par exemple, en cas de crash), il peut reprendre la partie à partir de l'état du jeu précédemment enregistré.
Installation
Clonez ce dépôt sur votre machine locale :

git clone https://github.com/TAKI12T/MorpionAveugle-
Accédez au répertoire du projet :

cd morpion-aveugle

Exécutez le serveur :
python main.py

Lancez les clients en fournissant l'adresse du serveur :
python main.py

Fonctionnalités:
Partie en réseau entre deux joueurs (client-serveur).
Mode Aveugle où les joueurs ne voient pas les coups adverses.
Possibilité de jouer plusieurs parties avec suivi des scores.
Observateurs qui peuvent suivre une partie en cours sans y participer.
Limitations:
Actuellement, le jeu supporte seulement deux joueurs à la fois, bien que des extensions pour plus de joueurs soient possibles.
Des améliorations sur la gestion des erreurs de connexion et la récupération d'état de jeu après une panne sont encore à peaufiner.

