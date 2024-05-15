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
        
    def _switch_player(self) -> None:
        self.current_player = -self.current_player
    
    def _is_game_over(self) -> bool:
        if all(self.board.board[i][j] != EMPTY for i,j in range(Board.BOARD_SIZE)):
            return True 
        for i,j in range(Board.BOARD_SIZE):
            if self._is_valid_move(i,j):
                return False   
        return True
            
    def _is_valid_move(self, row, col) -> bool:
        board = self.board.board
        if board[row][col] is not EMPTY:
            return False
        
        opponent_color = self.current_player
        for direction_row in [-1, 0, 1]:
            for direction_col in [-1, 0 , 1]:
                if direction_col == 0 and direction_row == 0:
                    continue # It's the same field - skip
                r,c = row + direction_row, col + direction_col
                if not (0 <= r < Board.BOARD_SIZE and 0 <= c < Board.BOARD_SIZE):
                    continue # Out of board   
                if board[r][c] == opponent_color:
                    # Move in this direction possible, continue checking further fields
                    while True:
                        r += direction_row
                        c += direction_col
                        if not (0 <= r < Board.BOARD_SIZE and 0 <= c < Board.BOARD_SIZE):
                            break # Out of board 
                        if board[r][c] == EMPTY:
                            break # Empty field on the other side - invalid move
                        if board[r][c] == self.current_player:
                            return True # This closes a line of current player's pieces - valid move
        return False
        
    def make_move(self, row, col) -> bool:
        if not self._is_valid_move(row, col):
            return False
        
        board = self.board.board
        opponenct_color = -self.current_player
        flip_list = []
        
        board[row, col] = self.current_player
        
        for direction_row in [-1, 0, 1]:
            for direction_col in [-1, 0, 1]:
                if direction_col == 0 and direction_row == 0:
                    continue # It's the same field - skip
                r, c = row + direction_row, col + direction_col
                while (0 <= r < Board.BOARD_SIZE and 0 <= c < Board.BOARD_SIZE) and board[r][c] == opponenct_color:
                    flip_list.append((r,c))
                    r += direction_row
                    c += direction_col
        for flip_row, flip_col in flip_list:
            board[flip_row][flip_col] = self.current_player
            
        self._switch_player()
        self.game_over = self._is_game_over()
        return True
    
    def print_board(self):
        self.board.print_board()