import math
import random
from typing import List, Optional
from game_logic.game import Game
from game_logic.constants import * # BLACK, WHITE

class GameState:
    def __init__(self, game: Game, last_move=None):
        self.game = game.copy()
        self.last_move = last_move

    def get_legal_moves(self) -> List:
        return self.game.get_legal_moves()

    def move(self, move) -> 'GameState':
        new_game_state = GameState(game = self.game, last_move = move) # Copy the game state
        assert(new_game_state.game.make_move(*move) == True)
        return new_game_state

    def is_terminal(self) -> bool:
        return self.game.is_game_over()

    def get_result(self) -> int:
        # assumes state is terminal
        return self.game.get_winner_int()

    def get_current_player(self) -> int:
        return self.game.current_player

    def get_last_move(self):
        return self.last_move

class Node:
    def __init__(self, state, parent: Optional['Node'] = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visit_count = 0
        self.win_count = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, exploration_value=1.414):
        best_value = -float('inf')
        best_nodes = []
        for child in self.children:
            uct_value = (child.win_count / child.visit_count) + exploration_value * math.sqrt(math.log(self.visit_count) / child.visit_count)
            if uct_value > best_value:
                best_value = uct_value
                best_nodes = [child]
            elif uct_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def add_child(self, child_state):
        child_node = Node(state=child_state, parent=self)
        self.children.append(child_node)
        return child_node

class MCTS:
    def __init__(self, state: GameState, iters=1000):
        self.root = Node(state)
        self.iters = iters

    def __init__(self, game: Game, iters=1000):
        self.root = Node(GameState(game))
        self.iters = iters

    def select(self, node: Node):
        while not node.state.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        return node

    def expand(self, node: Node):
        legal_moves = node.state.get_legal_moves()
        for move in legal_moves:
            new_state = node.state.move(move)
            if all(child.state != new_state for child in node.children):
                return node.add_child(new_state)
        return node

    def simulate(self, node: Node):
        current_state = node.state
        while not current_state.is_terminal():
            move = random.choice(current_state.get_legal_moves())
            current_state = current_state.move(move)
        return current_state.get_result()

    def backpropagate(self, node: Node, result):
        while node is not None:
            node.visit_count += 1
            if result == node.state.get_current_player():
                node.win_count += 1
            node = node.parent

    def move(self):
        for _ in range(self.iters):
            leaf = self.select(self.root)
            child = self.expand(leaf)
            result = self.simulate(child)
            self.backpropagate(child, result)
        return self.root.best_child(exploration_value=0).state.get_last_move()
    