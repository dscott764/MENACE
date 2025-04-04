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


def main():
    # Create a new board with all cells initialized to EMPTY.
    board = Board()

    # For demonstration, let's mark a few cells:
    # Set the top-left cell to X.
    board.set_cell(0, 0, Cell.X)
    # Set the center cell to O.
    board.set_cell(1, 1, Cell.O)
    # Set the bottom-right cell to X.
    board.set_cell(2, 2, Cell.X)

    # Print the board's current state.
    print("Board Representation:")
    print(board)
    print(board[2][2].value)

if __name__ == '__main__':
    main()
