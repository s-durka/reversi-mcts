from game_logic.constants import *

class Board:
    
    BOARD_SIZE = 8
    
    def __init__(self, initial_board = None):
        if initial_board is None:
            self.board = [[EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
            self.board[3][3] = self.board[4][4] = BLACK
            self.board[3][4] = self.board[4][3] = WHITE
        else:
            self.board = initial_board
        
    def copy(self):
        copied_board = [[cell for cell in row] for row in self.board]
        return Board(copied_board)
    
    def print_board(self) -> None:
        print("  0 1 2 3 4 5 6 7")
        for i in reversed(range(self.BOARD_SIZE)):
            print(i, end=' ')
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == BLACK:
                    print('B', end=' ')
                elif self.board[i][j] == WHITE:
                    print('W', end=' ')
                else:
                    print('.', end=' ')
            print()
            
    def black_count(self) -> int:
        return sum(row.count(BLACK) for row in self.board)

    def white_count(self) -> int:
        return sum(row.count(WHITE) for row in self.board)
            
    def is_in_range(self, row, column) -> bool:
        return 0 <= row < self.BOARD_SIZE and 0 <= column < self.BOARD_SIZE