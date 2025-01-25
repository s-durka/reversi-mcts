import argparse
from game_logic.game import Game
from ai_agents.minmax import Minimax
from game_logic.constants import *
from ai_agents.mcts import MCTS

def main_no_gui():
    mcts = MCTS(Game())
    parser = argparse.ArgumentParser(description="Reversi (Othello) Game")
    parser.add_argument('--agent', type=str, choices=['human', 'minimax', 'mcts'], default='human', help='Choose the agent to play against: human or minimax')
    parser.add_argument('--depth', type=int, default=5, help='Depth of the minimax algorithm')
    args = parser.parse_args()

    game = Game()
    minimax = Minimax(game, args.depth)
    while not game.game_over:
        game.print_board()
        if game.current_player == BLACK:
            print("Black's turn")
            row, col = map(int, input("Enter row and column: ").split())
            if not game.make_move(row, col):
                print("Invalid move. Try again.")
        else:
            if args.agent == 'human':
                print("White's turn")
                row, col = map(int, input("Enter row and column: ").split())
                if not game.make_move(row, col):
                    print("Invalid move. Try again.")
            elif args.agent == 'minimax':
                print("White's turn (AI)")
                move = minimax.best_move(game)
                if move:
                    game.make_move(*move)
            elif args.agent == 'mcts':
                print("White's turn (AI)")
                mcts = MCTS(game)
                move = mcts.move()
                assert(move is not None)
                if move:
                    game.make_move(*move)
    game.print_board()
    print("Game over!")

# if __name__ == "__main__":
#     main_no_gui()