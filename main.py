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
        Return a string representation of the board with horizontal
        lines.
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
        Return a string representation of the board state with
        horizontal lines.
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

if __name__ == '__main__':
    main()
