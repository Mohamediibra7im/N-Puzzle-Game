# N-Puzzle Game

## Overview

The N-Puzzle Game is a classic sliding puzzle implementation that supports various grid sizes (3x3, 4x4, 5x5) and multiple heuristic algorithms for solving the puzzle automatically. This project provides both a graphical interface (using PyQt5) and a robust puzzle-solving engine with different heuristic approaches.

## Features

### Core Functionality
- **Customizable Puzzle Sizes**: Play with 3x3, 4x4, or 5x5 grids
- **Interactive GUI**: Visual puzzle representation with tile movement
- **Automatic Solving**: AI solver using best-first search with selectable heuristics
- **Puzzle Generation**: Random shuffling to create new puzzles

### Heuristic Algorithms
1. **Misplaced Tiles**: Counts tiles not in their goal position
2. **Manhattan Distance**: Sum of distances each tile is from its goal position
3. **Linear Conflict**: Manhattan distance plus penalties for linear conflicts
4. **Nilsson's Sequence**: Special heuristic for 3x3 puzzles combining Manhattan distance with sequence scoring

### Technical Features
- State management with path reconstruction
- Search statistics tracking (nodes expanded, solution depth, etc.)
- Comprehensive unit testing

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/N-Puzzle-Game.git
   cd N-Puzzle-Game
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
python main.py
```

### Game Interface
- **Grid Display**: Shows the current puzzle state
- **Size Dropdown**: Select puzzle size (3x3, 4x4, 5x5)
- **Heuristic Dropdown**: Choose solving algorithm
- **Shuffle Button**: Randomize the puzzle
- **Solve Button**: Automatically solve the puzzle
- **Status Label**: Shows game messages and solving progress



## Architecture

### Key Components

1. **PuzzleState (puzzle.py)**
   - Represents the puzzle state
   - Handles tile movements and valid move generation
   - Tracks parent states for path reconstruction
   - Includes shuffle functionality

2. **Heuristics (heuristics.py)**
   - Various heuristic functions for estimating solution cost
   - All functions take a PuzzleState and return an integer

3. **Search Algorithm (search.py)**
   - Best-first search implementation
   - Uses a priority queue based on heuristic values
   - Tracks search statistics

4. **GUI (main.py)**
   - PyQt5-based interface
   - Visualizes puzzle state
   - Provides controls for puzzle manipulation

## Testing

The project includes comprehensive unit tests:

```bash
python test_all.py
```

Tests cover:
- Puzzle state manipulation
- Heuristic calculations
- Search algorithm functionality

## Performance Considerations

- The search algorithm has a default node limit of 100,000 to prevent excessive resource usage
- Larger puzzle sizes (4x4, 5x5) may require more time/memory to solve
- Different heuristics have varying performance characteristics:
  - Manhattan Distance is generally fast and effective.
  - Linear Conflict can find better solutions but is more computationally expensive.
  - Nilsson's Sequence is specialized for 3x3 puzzles.
  - Misplaced Tiles is simple but less effective for larger puzzles.

## Collebrators and Team Members

1. **Mohammed Ibrahim**
2. **Sarah Sayed**
3. **Mahmoud Gamal**
4. **Doha Mostafa**
5. **Yehia Khalid**
