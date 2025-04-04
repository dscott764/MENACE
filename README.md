# MENACE: Matchbox Educable Noughts and Crosses Engine Simulation

MENACE is a Python simulation of Donald Michie's innovative matchbox-based reinforcement learning system for playing Noughts and Crosses (Tic Tac Toe). This project emulates the original concept by using matchboxes and beads to represent and learn from legal moves, adapting its strategy over multiple games.

## Overview

- **Simulation:** MENACE learns by reinforcing moves that lead to wins and discouraging moves that result in losses.
- **Reinforcement Learning:** After each game, the algorithm adjusts the number of beads (representing moves) in each matchbox based on the outcome.
- **Canonical States:** The simulation uses symmetric transformations to reduce redundancy by converting board states into a canonical (lexicographically smallest) form resulting in 304 matchboxes just like the original engine.
- **Game Modes:** Run main.py and enter the number of games to automate. The opponent plays randomly, so it takes many games for the engine to get good. I used 100,000 games to see a significant difference.

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
