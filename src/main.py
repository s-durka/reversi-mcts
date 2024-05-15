from game_logic.game import Game

def main():
    game = Game()
    game.print_board()
    result = game.make_move(2,4)
    game.print_board()

main()