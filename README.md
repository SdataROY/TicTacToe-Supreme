# TicTacToe Supreme

This is a modern implementation of the classic TicTacToe game using Python and Pygame inspired by Google. The game features a 4x4 grid, enhanced visuals, score tracking, and a new set of rules for winning including rows, columns, diagonals, and squares.

## Features
- **Simple Controls**: Click on the grid to place your marker.
- **Score Tracking**: Scores for Player X and Player O, and the number of draws are displayed at the top.
- **Dynamic Turn Indicator**: Displays whose turn it is with a distinct color for each player.
- **Winning Conditions**: Highlights the winning line or square in the respective player's color.
- **Reset Capability**: Automatically resets the game after a win or draw.

## Requirements
To run this game, you need Python and Pygame installed on your system. Python 3.6 or higher is recommended for better compatibility. You can install Pygame using pip:

```bash
pip install pygame
```

## Running the Game
To start the game, run the Python script from your terminal or command prompt:

```bash
python TicTacToe.py
```
Ensure that the script name matches the actual name of your Python file.

## Controls
- **Mouse Click**: Place your marker (X or O) on the clicked grid cell.
- **Turn Change**: The turn will automatically change to the next player after each click.
- **Automatic Reset**: The game updates the score and resets for a new round after a win or draw.

## Rules for Winning
A player wins the game if they achieve any of the following conditions with their markers (X or O):

- **Horizontal Line**: Place four markers in a horizontal row.
- **Vertical Line**: Place four markers in a vertical column.
- **Diagonal Line**: Place four markers in a diagonal line from one corner of the grid to another.
- **Square Formation**: Place four markers in a 2x2 square formation anywhere on the grid.
- **Corners**: Place markers in all four corners of the grid.

## Enjoy the Game
Enjoy playing TicTacToe Supreme and try to outsmart your opponent with clever moves and strategies!
