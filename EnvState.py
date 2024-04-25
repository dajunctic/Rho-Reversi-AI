#!/bin/python3 
from distutils.command.build import build
from re import S
import string


# A generic discrete static known environment 
class GenericEnvironment:
    def __init__(self) -> None:
        pass

# TODO: make Reversi inherit GenericEnvironment 
class Reversi: 
    DARK, LIGHT, NODISC = 0, 1, -1
    SYMBOLS = ['X', 'O', ' ']
    BOARD_SIZE = 8
    PLAYER_COUNT = 2
    def __init__(self) -> None: 
        self.board = [Reversi.NODISC for _ in range(Reversi.BOARD_SIZE**2)]

        self.board[self.sqr(Reversi.BOARD_SIZE // 2, Reversi.BOARD_SIZE // 2 - 1)] = Reversi.DARK
        self.board[self.sqr(Reversi.BOARD_SIZE // 2 - 1, Reversi.BOARD_SIZE // 2)] = Reversi.DARK

        self.board[self.sqr(Reversi.BOARD_SIZE // 2, Reversi.BOARD_SIZE // 2)] = Reversi.LIGHT
        self.board[self.sqr(Reversi.BOARD_SIZE // 2 - 1, Reversi.BOARD_SIZE // 2 - 1)] = Reversi.LIGHT

        self.prev_player = -1
        self.player = Reversi.DARK

        self.legal = set()
        self.last_player_pass = False
        self.__enumerate_legal_action()

        self.last_action = ()
        self.t : int = 0
        
        
        self.board2D = [[0 for j in range(Reversi.BOARD_SIZE)] for i in range(Reversi.BOARD_SIZE)]
        self.buildBoard2D()

        
    def __enumerate_legal_action(self): 
        for row in range(Reversi.BOARD_SIZE): 
            for col in range(Reversi.BOARD_SIZE):
                center_value = self.board[self.sqr(row, col)]
                if center_value != self.player:
                    continue
                for d_row in range(-1, 2):
                    for d_col in range(-1, 2):
                        if d_row == 0 and d_col == 0:
                            continue 
                        cursor_row = row + d_row 
                        cursor_col = col + d_col
                        length = 0
                        while 0 <= cursor_row < Reversi.BOARD_SIZE and 0 <= cursor_col < Reversi.BOARD_SIZE: 
                            index = self.sqr(cursor_row, cursor_col)
                            if self.board[index] == center_value:
                                length = -1
                                break 
                            if self.board[index] == Reversi.NODISC:
                                break 
                            length += 1
                            cursor_row += d_row 
                            cursor_col += d_col 
                        if length > 0: 
                            if not (0 <= cursor_row < Reversi.BOARD_SIZE and 0 <= cursor_col < Reversi.BOARD_SIZE):
                                continue
                            self.legal.add((cursor_row, cursor_col))
                            continue
        if len(self.legal) == 0 and (not self.last_player_pass):
            self.legal.add((-1, -1))

    def __str__(self) -> str: 
        result = "   | "
        result += " | ".join(string.ascii_uppercase[0:Reversi.BOARD_SIZE])
        result += " |\n"
        for row in range(Reversi.BOARD_SIZE):
            result += "{}".format("---+" * (Reversi.BOARD_SIZE + 1)) + "---\n"
            result += ' {} |'.format(row + 1)
            for col in range(Reversi.BOARD_SIZE): 
                result += " {} |".format(Reversi.SYMBOLS[self.board[self.sqr(row, col)]])
            result += ' {} \n'.format(row + 1)
        result += "---+" * (Reversi.BOARD_SIZE + 1) + "---\n   | "
        result += " | ".join(string.ascii_uppercase[0:Reversi.BOARD_SIZE])
        result += " | "
        
        
        # Build Board 2 - Dimension 
        self.buildBoard2D()
                    
        
        return result
    
    def buildBoard2D(self):
        for row in range(Reversi.BOARD_SIZE):
            for col in range(Reversi.BOARD_SIZE): 
                if Reversi.SYMBOLS[self.board[self.sqr(row, col)]] == 'X':
                    self.board2D[row][col] = 1
                if Reversi.SYMBOLS[self.board[self.sqr(row, col)]] == 'O':
                    self.board2D[row][col] = 2

    def sqr(self, row: int, col: int) -> int:
        try:
            assert 0 <= row < Reversi.BOARD_SIZE 
            assert 0 <= col < Reversi.BOARD_SIZE 
            return row * Reversi.BOARD_SIZE + col 
        except:
            print("{} {}".format(row, col))
            assert False 


    def act(self, action: tuple[int, int]): #NOTE: Performance improvement, cache the directions in which the discs needed to be flipped
        assert action in self.legal
        self.t += 1
        self.last_action = action
        row, col = action[0], action[1]
        if row != -1: 
            self.last_player_pass = False
            self.board[self.sqr(row, col)] = self.player
            for d_row in range(-1, 2):
                for d_col in range(-1, 2):
                    if d_col == 0 and d_row == 0:
                        continue 
                    cursor_row, cursor_col = row + d_row, col + d_col 
                    while 0 <= cursor_row < Reversi.BOARD_SIZE and 0 <= cursor_col < Reversi.BOARD_SIZE: 
                        index = self.sqr(cursor_row, cursor_col)
                        if self.board[index] == Reversi.NODISC: 
                            cursor_row, cursor_col = row, col
                            break 
                        if self.board[index] == self.player:
                            break
                        cursor_row += d_row 
                        cursor_col += d_col 
                    while (cursor_row != row or cursor_col != col) and (0 <= cursor_row < Reversi.BOARD_SIZE and 0 <= cursor_col < Reversi.BOARD_SIZE):  
                        index = self.sqr(cursor_row, cursor_col)
                        self.board[index] = self.player
                        cursor_row -= d_row 
                        cursor_col -= d_col
        else:
            self.last_player_pass = True

        self.prev_player = self.player
        self.player = (self.player + 1) % 2
        
        self.legal.clear()
        self.__enumerate_legal_action()
    
    def tally(self) -> int:
        return self.board.count(Reversi.DARK) - self.board.count(Reversi.LIGHT)

    def result(self) -> int: 
        t = self.tally() 
        if t > 0: 
            return Reversi.DARK 
        elif t < 0:
            return Reversi.LIGHT 
        else: 
            return Reversi.NODISC

    @staticmethod
    def acttostr(action: tuple[int, int]) -> str: 
        try:
            assert 0 <= action[0] < Reversi.BOARD_SIZE 
            assert 0 <= action[1] < Reversi.BOARD_SIZE
            return "{}{}".format(string.ascii_uppercase[action[1]], action[0] + 1)
        except: 
            assert action == (-1, -1)
            return "PASS"

    @staticmethod 
    def strtoact(alphanum: str) -> tuple[int, int]:
        if alphanum.upper() == "PASS":
            return (-1, -1)
        action = (int(alphanum[1]) - 1, string.ascii_uppercase.find(alphanum[0].upper()))
        assert 0 <= action[0] < Reversi.BOARD_SIZE 
        assert 0 <= action[1] < Reversi.BOARD_SIZE
        return action


if __name__ == "__main__":
    test = Reversi() 
    for action in test.legal: 
        print(Reversi.acttostr(action))
    print("\n")
    print(Reversi.strtoact("C4") in test.legal)
    test.act((3, 2))
    print(test)
    print(Reversi.strtoact("E1"))
