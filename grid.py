
#!/usr/bin/python3

symbols = [' ', 'O', 'X']
EMPTY = 0
J1 = 1
J2 = 2
NB_CELLS = 9

class grid:
    def __init__(self):
        self.cells = [EMPTY] * NB_CELLS

    def play(self, player, cellNum):
        assert 0 <= cellNum < NB_CELLS
        assert self.cells[cellNum] == EMPTY
        self.cells[cellNum] = player

    def display(self):
        print("-------------")
        for i in range(3):
            print("|", symbols[self.cells[i * 3]], "|", symbols[self.cells[i * 3 + 1]], "|", symbols[self.cells[i * 3 + 2]], "|")
            print("-------------")

    def display_string(self):
        result = "-------------\n"
        for i in range(3):
            result += f"| {symbols[self.cells[i * 3]]} | {symbols[self.cells[i * 3 + 1]]} | {symbols[self.cells[i * 3 + 2]]} |\n"
            result += "-------------\n"
        return result

    def winner(self, player):
        assert player in (J1, J2)
        for y in range(3):
            if self.cells[y * 3] == player and self.cells[y * 3 + 1] == player and self.cells[y * 3 + 2] == player:
                return True
        for x in range(3):
            if self.cells[x] == player and self.cells[3 + x] == player and self.cells[6 + x] == player:
                return True
        if self.cells[0] == player and self.cells[4] == player and self.cells[8] == player:
            return True
        if self.cells[2] == player and self.cells[4] == player and self.cells[6] == player:
            return True
        return False

    def gameOver(self):
        if self.winner(J1):
            return J1
        if self.winner(J2):
            return J2
        if all(cell != EMPTY for cell in self.cells):
            return 0
        return -1