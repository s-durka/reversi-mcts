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
        
    def copy(self):
        copied_game = Game()
        copied_game.board = self.board.copy()
        copied_game.current_player = self.current_player
        copied_game.game_over = self.game_over
        return copied_game
        
    def _switch_player(self) -> None:
        self.current_player = -self.current_player
    
    def is_game_over(self) -> bool:
        if all(self.board.board[i][j] != EMPTY for i in range(Board.BOARD_SIZE) for j in range(Board.BOARD_SIZE)):
            return True 
        for i in range(Board.BOARD_SIZE):
            for j in range(Board.BOARD_SIZE):
                if self.is_valid_move(i,j):
                    return False   
        return True
            
    def is_valid_move(self, row, col) -> bool:
        board = self.board.board
        if board[row][col] is not EMPTY:
            return False
        
        opponent_color = -self.current_player
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
                        if not self.board.is_in_range(r,c):
                            break # Out of board 
                        if board[r][c] == EMPTY:
                            break # Empty field on the other side - invalid move
                        if board[r][c] == self.current_player:
                            return True # This closes a line of current player's pieces - valid move
        return False
        
    def make_move(self, row, col) -> bool:
        if not self.is_valid_move(row, col):
            return False
        
        board = self.board.board
        opponent_color = -self.current_player
        flip_list = []
        
        board[row][col] = self.current_player
        
        for direction_row in [-1, 0, 1]:
            for direction_col in [-1, 0, 1]:
                if direction_col == 0 and direction_row == 0:
                    continue # It's the same field - skip
                potential_flips = []
                r, c = row + direction_row, col + direction_col
                if not self.board.is_in_range(r,c):
                    continue
                while (self.board.is_in_range(r + direction_row, c + direction_col)) and board[r][c] == opponent_color:
                    potential_flips.append((r,c))
                    r += direction_row
                    c += direction_col
                if board[r][c] == self.current_player:
                    flip_list.extend(potential_flips) # Only flip if there is a piece to close the line       
        for flip_row, flip_col in flip_list:
            board[flip_row][flip_col] = self.current_player
            
        self._switch_player()
        self.game_over = self.is_game_over()
        return True
    
    def evaluate_board(self):
        score = 0
        for row in self.board.board:
            for cell in row:
                if cell == self.current_player:
                    score += 1
                elif cell == -self.current_player:
                    score -= 1
        return score
    
    def get_winner(self) -> str:
        if self.game_over:
            return "WHITE" if self.board.white_count() > self.board.black_count() else "BLACK"
        return None
    
    def get_black_count(self) -> int:
        return self.board.black_count()
    
    def get_white_count(self) -> int:
        return self.board.white_count()
    
    def print_board(self):
        self.board.print_board()