# MENACE: Matchbox Educable Noughts and Crosses Engine Simulation

MENACE is a Python simulation of Donald Michie's innovative matchbox-based reinforcement learning system for playing Noughts and Crosses (Tic Tac Toe). This project emulates the original concept by using matchboxes and beads to represent and learn from legal moves, adapting its strategy over multiple games.

## Overview

- **Simulation:** MENACE learns by reinforcing moves that lead to wins and discouraging moves that result in losses.
- **Reinforcement Learning:** After each game, the algorithm adjusts the number of beads (representing moves) in each matchbox based on the outcome.
- **Canonical States:** The simulation uses symmetric transformations to reduce redundancy by converting board states into a canonical (lexicographically smallest) form resulting in 304 matchboxes just like the original engine.
- **Game Modes:** Enter the number of games to automate. The opponent plays randomly. As the machine gets better, the opponent's percentage of wins will decrease.
## Features

- **Board Representation:** A 3x3 grid using a custom `Cell` enum for tracking moves.
- **Matchbox Mechanism:** Each matchbox contains beads corresponding to legal moves for a given board state.
- **Learning Update:** Adjusts bead counts based on win, loss, or draw outcomes.
- **Self-Documenting Code:** Clean, modular design with clear class responsibilities (e.g., `Board`, `BoardState`, `Matchbox`, `MENACEEngine`).

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/dscott764/MENACE.git

You’ll be prompted to enter the number of games to simulate. The program will then run the specified number of games between MENACE (playing as O) and a random opponent (playing as X), displaying the game outcomes and statistics at the end.

## How It Works

1. Board & Game Setup:
The board is represented as a 3x3 grid. MENACE uses a matchbox for each unique board state where it is its turn to play.
2. Move Selection:
For every legal move (i.e., moves into empty cells), the corresponding matchbox contains a number of beads. MENACE selects a move at random from these beads.
3. Learning Mechanism:
* Win: Add a bead to reinforce the winning move.
* Loss: Remove a bead to discourage the move (ensuring at least one bead remains).
* Draw: No changes are made.
4. Symmetry Reduction:
To avoid redundant matchboxes, the board state is transformed into its canonical form using rotations and reflections.
