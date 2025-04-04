"""
MENACE: Matchbox Educable Noughts and Crosses Engine Simulation

This module simulates Donald Michie's MENACE, an early example of a
machine learning system for playing Noughts and Crosses using a
matchbox-based reinforcement learning approach. It features a
self-documenting design with clearly defined classes such as Board and
Cell, ensuring that the game board is always a valid 3x3 grid with
restricted values.

Usage:
    - Run the module to start a simulation of Noughts and Crosses
      games.
"""
import random
from enum import Enum


class Cell(Enum):
    """
    Represents the state of a cell in a Noughts and Crosses board.

    Attributes:
        EMPTY: An empty cell.
        O: A cell occupied by O.
        X: A cell occupied by X.
    """
    EMPTY = ' '
    O     = 'O'
    X     = 'X'


class Board:
    """
    Represents a 3x3 Noughts and Crosses board for MENACE. Each cell
    is restricted to be an instance of Cell.
    """
    def __init__(self, grid=None):
        if grid is None:
            # Create a 3x3 grid initialized with Cell.EMPTY
            self.grid = [
                [Cell.EMPTY for _ in range(3)] for _ in range(3)
            ]
        else:
            if len(grid) != 3 or any(len(row) != 3 for row in grid):
                raise ValueError("Grid must be 3x3")
            for row in grid:
                for cell in row:
                    if not isinstance(cell, Cell):
                        raise ValueError(
                            "All elements must be instances of Cell")
            self.grid = grid

    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        if not isinstance(value, list) or len(value) != 3:
            raise ValueError("Row must be a list of 3 Cell elements")
        for cell in value:
            if not isinstance(cell, Cell):
                raise ValueError("All elements must be instances of Cell")
        self.grid[index] = value

    def get_cell(self, row, col):
        """Retrieve the cell at the specified row and column."""
        return self.grid[row][col]

    def set_cell(self, row, col, cell):
        """Set the cell at the specified row and column."""
        if not isinstance(cell, Cell):
            raise ValueError("Value must be an instance of Cell")
        self.grid[row][col] = cell

    def __str__(self):
        """
        Return a string representation of the board.
        """
        board_lines = []
        for i, row in enumerate(self.grid):
            board_lines.append(" | ".join(cell.value for cell in row))
            if i < len(self.grid) - 1:
                board_lines.append("---------")
        return "\n".join(board_lines)


class BoardState:
    """
    Represents an immutable snapshot of a 3x3 Noughts and Crosses board.
    The internal representation is a tuple of tuples, ensuring immutability.
    """
    def __init__(self, grid=None):
        if grid is None:
            # Create a 3x3 grid initialized with Cell.EMPTY
            self.grid = tuple(tuple(Cell.EMPTY for _ in range(3)) for _ in range(3))
        else:
            if len(grid) != 3 or any(len(row) != 3 for row in grid):
                raise ValueError("Grid must be 3x3")
            new_grid = []
            for row in grid:
                new_row = []
                for cell in row:
                    if not isinstance(cell, Cell):
                        raise ValueError("All elements must be instances of Cell")
                    new_row.append(cell)
                new_grid.append(tuple(new_row))
            self.grid = tuple(new_grid)

    def get_cell(self, row, col):
        """Retrieve the cell at the specified row and column."""
        return self.grid[row][col]

    def __getitem__(self, index):
        """
        Allow indexing to retrieve entire rows from the board
        state.
        """
        return self.grid[index]

    def __str__(self):
        """
        Return a string representation of the board state.
        """
        board_lines = []
        for i, row in enumerate(self.grid):
            board_lines.append(" | ".join(cell.value for cell in row))
            if i < len(self.grid) - 1:
                board_lines.append("---------")
        return "\n".join(board_lines)

    def __eq__(self, other):
        if isinstance(other, BoardState):
            return self.grid == other.grid
        return False

    def __hash__(self):
        return hash(self.grid)


class Bead:
    """
    Represents a single bead corresponding to a move in MENACE.

    Attributes:
        move (tuple): A tuple (row, col) indicating the move this bead
                      represents.
    """
    def __init__(self, move):
        if not (isinstance(move, tuple) and len(move) == 2):
            raise ValueError("Move must be a tuple of (row, col)")
        self.move = move

    def __str__(self):
        return f"Bead(move={self.move})"

    def __repr__(self):
        return str(self)


class Matchbox:
    """
    Represents a matchbox in MENACE, containing a BoardState and a
    collection of beads corresponding to legal moves from that state.

    The matchbox is associated with a specific board state and holds
    beads for every legal move (i.e., moves into empty cells). The
    weight of a move is determined by the number of beads representing
    that move.
    """
    def __init__(self, board_state, initial_bead_count=3):
        if not isinstance(board_state, BoardState):
            raise ValueError("board_state must be an instance of BoardState")
        self.board_state = board_state
        self.beads = []
        
        # Determine legal moves: iterate over all cells and check for
        # emptiness.
        for row in range(3):
            for col in range(3):
                if board_state.get_cell(row, col) == Cell.EMPTY:
                    # Add initial_bead_count beads for each legal
                    # move.
                    for _ in range(initial_bead_count):
                        self.beads.append(Bead((row, col)))
                        
    def add_beads(self, move, count=1):
        """
        Add a specified number of beads corresponding to the given
        move.
        
        Args:
            move (tuple): A tuple (row, col) representing the move.
            count (int): The number of beads to add.
        """
        # Check if the move is legal in the board state.
        if self.board_state.get_cell(*move) != Cell.EMPTY:
            raise ValueError("Move is not legal in this board state")
        for _ in range(count):
            self.beads.append(Bead(move))
    
    def remove_beads(self, move, count=1):
        """
        Remove up to a specified number of beads for the given move by
        going over the beads and skipping the ones to be removed.
        
        If fewer than count beads exist for that move, remove all of
        them.
        
        Args:
            move (tuple): A tuple (row, col) representing the move.
            count (int): The maximum number of beads to remove.
        """
        removed = 0
        new_beads = []
        for bead in self.beads:
            if removed < count and bead.move == move:
                removed += 1
            else:
                new_beads.append(bead)
        self.beads = new_beads
    
    def get_bead_count(self, move):
        """
        Return the number of beads corresponding to the given move.
        
        Args:
            move (tuple): A tuple (row, col) representing the move.
            
        Returns:
            int: The number of beads for that move.
        """
        return sum(1 for bead in self.beads if bead.move == move)
    
    def __str__(self):
        """
        Return a string representation of the matchbox, including the
        board state
        and the counts of beads per move.
        """
        # Group the beads by move and count them.
        move_counts = {}
        for bead in self.beads:
            move_counts[bead.move] = move_counts.get(bead.move, 0) + 1
        moves_str = ', '.join(
            f"{move}: {count}" for move, count in move_counts.items())
        return f"Matchbox for board state:\n{self.board_state}\nBeads: {moves_str}"


def check_winner(board):
    """
    Check the board for a winner.
    Returns:
      - 'MENACE' if MENACE (playing as O) wins,
      - 'opponent' if the opponent (playing as X) wins,
      - 'draw' if the board is full with no winner,
      - None if the game is still in progress.
    """
    lines = []
    grid = board.grid
    # rows
    lines.extend(grid)
    # columns
    lines.extend([[grid[r][c] for r in range(3)] for c in range(3)])
    # diagonals
    lines.append([grid[i][i] for i in range(3)])
    lines.append([grid[i][2 - i] for i in range(3)])
    
    for line in lines:
        if all(cell == Cell.O for cell in line):
            return 'MENACE'
        if all(cell == Cell.X for cell in line):
            return 'opponent'
    # Check for draw (no empty cells left)
    if all(cell != Cell.EMPTY for row in grid for cell in row):
        return 'draw'
    return None


class MENACEEngine:
    """
    MENACEEngine simulates Donald Michie's MENACE learning algorithm 
    for playing Noughts and Crosses using a matchbox-based
    reinforcement learning approach.
    """
    def __init__(self, initial_bead_count=3):
        # Map BoardState -> Matchbox
        self.matchboxes = {}
        self.initial_bead_count = initial_bead_count
        # History of moves made during the current game: list of
        # (matchbox, move)
        self.game_history = []
        
    def get_matchbox(self, board_state):
        """
        Retrieve the matchbox for a given board state. If it doesn't
        exist, create it.
        """
        if board_state not in self.matchboxes:
            self.matchboxes[board_state] = Matchbox(
                board_state, self.initial_bead_count)
        return self.matchboxes[board_state]
    
    def choose_move(self, board_state):
        """
        Choose a move based on the beads in the matchbox corresponding
        to the given board state.
        """
        matchbox = self.get_matchbox(board_state)
        if not matchbox.beads:
            raise ValueError("No legal moves available in matchbox")
        selected_bead = random.choice(matchbox.beads)
        # Record the matchbox and move so we can adjust later
        self.game_history.append((matchbox, selected_bead.move))
        return selected_bead.move
    
    def update_learning(self, outcome):
        """
        Update the matchboxes based on the outcome of the game.
        
        Outcome is:
          1 for win,
          0 for draw,
         -1 for loss.
        
        Update strategy:
          - If win, add a bead to each matchbox used.
          - If loss, remove a bead from each matchbox used (if
            possible).
          - For a draw, make no changes.
        """
        for matchbox, move in self.game_history:
            if outcome == 1:
                matchbox.add_beads(move, count=1)
            elif outcome == -1:
                # Remove a bead if there's more than one (to avoid
                # removing all moves)
                if matchbox.get_bead_count(move) > 1:
                    matchbox.remove_beads(move, count=1)
        self.game_history = []  # Clear history after learning
    
    def play_game(self, opponent_move_func):
        """
        Simulate a game between MENACE and an opponent.
        
        The opponent_move_func is a function that takes a Board object
        and returns a move (row, col). For simplicity, MENACE plays as
        'O' and the opponent as 'X'.
        """
        board = Board()
        current_player = 'MENACE'
        self.game_history = []  # Reset history at the start of the
                                # game
        
        while True:
            board_state = BoardState(board.grid)
            if current_player == 'MENACE':
                move = self.choose_move(board_state)
                board.set_cell(move[0], move[1], Cell.O)
            else:
                move = opponent_move_func(board)
                board.set_cell(move[0], move[1], Cell.X)
            
            print(board)
            print()
            
            result = check_winner(board)
            if result:
                if result == 'MENACE':
                    self.update_learning(1)
                elif result == 'opponent':
                    self.update_learning(-1)
                else:
                    self.update_learning(0)
                return result
            
            # Alternate turns
            current_player = ('opponent' if current_player == 'MENACE' 
                              else 'MENACE')


def random_opponent_move(board):
    """
    Simple opponent strategy: randomly select one of the available
    legal moves.
    """
    legal_moves = [(r, c) for r in range(3) for c in range(3) 
                   if board.get_cell(r, c) == Cell.EMPTY]
    return random.choice(legal_moves)


def main():
    engine = MENACEEngine(initial_bead_count=3)
    result = engine.play_game(random_opponent_move)
    print("Winner:", result)


if __name__ == '__main__':
    main()
