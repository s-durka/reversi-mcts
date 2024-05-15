from game_logic.board import Board
from game_logic.constants import *

class Game:
    
    board: Board
    current_player: int
    game_over: bool
    
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        
    def is_valid_move(self, row, col) -> bool:
        if self.board[row][col] is not EMPTY:
            return False
        pass
    
    def switch_player(self):
        self.current_player = -self.current_player
    
    def print_board(self):
        self.board.print_board()