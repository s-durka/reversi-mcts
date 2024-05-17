from game_logic.constants import *
class Board:
    
    BOARD_SIZE = 8
    
    def __init__(self):
        self.board = [[EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.board[3][3] = self.board[4][4] = BLACK
        self.board[3][4] = self.board[4][3] = WHITE
        
    def copy(self):
        copied_board = [[cell for cell in row] for row in self.board]
        return Board(copied_board)
    
    def print_board(self) -> None:
        print("  A B C D E F G H")
        for i in reversed(range(self.BOARD_SIZE)):
            print(i + 1, end=' ')
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == BLACK:
                    print('B', end=' ')
                elif self.board[i][j] == WHITE:
                    print('W', end=' ')
                else:
                    print('.', end=' ')
            print()