from game_logic.game import Game
from game_logic.board import Board

class Minimax:
    game: Game
    
    def __init__(self, game: Game, depth=5):
        self.game = game
        self.depth = depth
        
    def minimax(self, game: Game, depth: int, alpha, beta, maximizing_player: bool) -> int:
        if depth == 0 or game.game_over:
            return game.evaluate_board()
    
        valid_moves = [(r, c) for r in range(Board.BOARD_SIZE) for c in range(Board.BOARD_SIZE) if game.is_valid_move(r, c)]
        if not valid_moves:
            return game.evaluate_board(game.board.board, game.current_player), None
    
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_game = game.copy()
                new_game.make_move(*move)
                eval = self.minimax(new_game, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_game = game.copy()
                new_game.make_move(*move)
                eval = self.minimax(new_game, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def best_move(self, game):
        best_eval = float('-inf')
        best_move = None
        for move in [(r, c) for r in range(Board.BOARD_SIZE) for c in range(Board.BOARD_SIZE) if game.is_valid_move(r, c)]:
            new_game = game.copy()
            new_game.make_move(*move)
            move_eval = self.minimax(new_game, self.depth - 1, float('-inf'), float('inf'), False)
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        return best_move