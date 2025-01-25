import tkinter as tk
from gui.reversi_gui import ReversiGUI
from game_logic.constants import *

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Reversi (Othello) Game")
    parser.add_argument('--agent', type=str, choices=['human', 'minimax', 'mcts'], default='mcts', help='Choose your opponent: human or AI (MCTS or Minimax)')
    parser.add_argument('--depth', type=int, default=5, help='Depth of the minimax algorithm')

    args = parser.parse_args()

    root = tk.Tk()
    gui = ReversiGUI(root, minimax_depth=args.depth, agent=args.agent)
    root.mainloop()

if __name__ == "__main__":
    main()