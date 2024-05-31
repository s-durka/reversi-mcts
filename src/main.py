import argparse
from game_logic.game import Game
from ai_agents.minmax import Minimax
from game_logic.constants import *

def main():
    parser = argparse.ArgumentParser(description="Reversi (Othello) Game")
    parser.add_argument('--agent', type=str, choices=['human', 'minimax'], default='human', help='Choose the agent to play against: human or minimax')
    parser.add_argument('--depth', type=int, default=5, help='Depth of the minimax algorithm')
    args = parser.parse_args()

    game = Game()
    minimax = Minimax(game)
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
                move = minimax.best_move(game, args.depth)
                if move:
                    game.make_move(*move)

    game.print_board()
    print("Game over!")

if __name__ == "__main__":
    main()