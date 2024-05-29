import tkinter as tk
from gui.reversi_gui import ReversiGUI
from game_logic.constants import *

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Reversi (Othello) Game")
    parser.add_argument('--agent', type=str, choices=['human', 'minimax'], default='human', help='Choose the agent to play against: human or minimax')
    parser.add_argument('--depth', type=int, default=5, help='Depth of the minimax algorithm')
    args = parser.parse_args()

    root = tk.Tk()
    gui = ReversiGUI(root, agent=args.agent, depth=args.depth)
    root.mainloop()

if __name__ == "__main__":
    main()