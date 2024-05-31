import tkinter as tk
from tkinter import messagebox
from game_logic.constants import *
from game_logic.game import Game
from game_logic.board import Board
from ai_agents.minmax import Minimax

class ReversiGUI:
    def __init__(self, root, agent='human', depth=5):
        self.root = root
        self.root.title("Reversi (Othello)")

        self.game = Game()
        self.minimax = Minimax(self.game)
        self.agent = agent
        self.depth = depth

        self.canvas_size = 600
        self.cell_size = self.canvas_size // 8

        # Create a frame to hold the piece count and game board
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Add labels to show the piece count
        self.black_label = tk.Label(self.frame, text=f"Black: {self.game.get_black_count()}", font=("Helvetica", 14))
        self.black_label.grid(row=0, column=0, padx=(20, 0), pady=10, sticky='w')

        self.white_label = tk.Label(self.frame, text=f"White: {self.game.get_white_count()}", font=("Helvetica", 14))
        self.white_label.grid(row=0, column=1, padx=(0, 20), pady=10, sticky='e')

        self.canvas = tk.Canvas(self.frame, width=self.canvas_size, height=self.canvas_size, bg='green')
        self.canvas.grid(row=1, column=0, columnspan=2)

        self.canvas.bind("<Button-1>", self.click_handler)

        self.update_board()

    def click_handler(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        self.process_move(row, col)

    def create_board(self):
        for row in range(8):
            for col in range(8):
                button = tk.Button(self.root, width=4, height=2, command=lambda r=row, c=col: self.process_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def process_move(self, row, col):
        if self.game.current_player == BLACK:
            if self.game.make_move(row, col):
                self.update_board()
                if not self.game.game_over:
                    self.root.after(1000, self.ai_move)
        elif self.agent == 'human':
            if self.game.make_move(row, col):
                self.update_board()
        else:
            print("Invalid move. Try again.")

    def ai_move(self):
        if self.agent == 'minimax' and self.game.current_player == WHITE:
            move = self.minimax.best_move(self.game, self.depth)
            if move:
                self.game.make_move(*move)
                self.update_board()

    def update_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='#005000')

                piece = self.game.board.board[row][col]
                if piece == BLACK:
                    self.draw_piece(row, col, 'black')
                elif piece == WHITE:
                    self.draw_piece(row, col, 'white')

        self.black_label.config(text=f"Black: {self.game.get_black_count()}")
        self.white_label.config(text=f"White: {self.game.get_white_count()}")

        if self.game.game_over:
            self.show_winner_message()
    
    def show_winner_message(self, winner):
        # Calculate dimensions for the message box
        box_width = self.canvas_size * 0.8
        box_height = 100
        box_x1 = (self.canvas_size - box_width) / 2
        box_y1 = (self.canvas_size - box_height) / 2
        box_x2 = box_x1 + box_width
        box_y2 = box_y1 + box_height

        # Darken the game board
        self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill='black', stipple='gray50')

        # Draw the main message box with opacity
        self.canvas.create_rectangle(box_x1, box_y1, box_x2, box_y2, fill='black', outline='black')

        # Draw the winner text
        self.canvas.create_text(self.canvas_size / 2, (self.canvas_size / 2), text=f"Winner: {winner}", font=("Helvetica", 20, "bold"), fill="white")

    def draw_piece(self, row, col, color):
        x1 = col * self.cell_size + 5
        y1 = row * self.cell_size + 5
        x2 = (col + 1) * self.cell_size - 5
        y2 = (row + 1) * self.cell_size - 5
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)