#!/usr/bin/python3

from grid import *
import  random

def main():
    grids = [grid(), grid(), grid()]
    current_player = J1
    grids[J1].display()
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input (f"joueur {current_player} : quel case allez-vous jouer ?"))
        if current_player == J2:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input (f"joueur {current_player} : quel case allez-vous jouer ?"))
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        if current_player == J1:
            grids[J1].display()
        if current_player == J2:
            grids[J2].display()
    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print(f"Player {J1} win !")
    else:
        print(f"Player {J1} loose !")
    if grids[0].gameOver() == J2:
        print(f"Player {J2} win !")
    else:
        print(f"Player {J2} loose !")

main()
