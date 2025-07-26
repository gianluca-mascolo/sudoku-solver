# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based Sudoku solver with a text-based user interface (TUI) built using the Textual framework. The solver implements various Sudoku solving algorithms and provides an interactive interface for entering and solving puzzles.

## Common Commands

### Development Setup
```bash
make setup          # Install dependencies with poetry and set up pre-commit hooks
poetry install      # Alternative: install dependencies directly
```

### Code Quality
```bash
make format         # Run black, isort, and flake8 formatters/linters
poetry run black .  # Format code (line length: 200)
poetry run isort .  # Sort imports
poetry run flake8 . # Run linter
```

### Testing
```bash
make test                    # Run all tests
poetry run pytest            # Alternative: run all tests
poetry run pytest -k test_valid  # Run specific test by name
```

### Running the Application
```bash
make sudoku         # Run the TUI application
poetry run sudoku   # Alternative: run directly via poetry
./sudoku.py         # Legacy CLI interface (reads s.txt, outputs to sol.txt)
```

## Architecture

### Core Components

1. **SudokuBoard** (`sudokulib.py`): Core data structure representing a 9x9 Sudoku board
   - Each cell is a set of possible values (1-9)
   - Provides validation and cell management methods

2. **Solving Engine** (`sudokulib.py`): Implements multiple solving strategies
   - Basic elimination (removing solved values from neighbors)
   - Hidden singles detection
   - Naked pairs/triples elimination
   - Hidden pairs elimination
   - Backtracking for complex puzzles

3. **TUI Application** (`sudoku.py`): Interactive interface using Textual
   - Grid navigation with keyboard
   - File loading from samples directory (L key)
   - Save current puzzle to file (W key)
   - Real-time validation
   - Solve command integration

### Key Functions
- `neighbor(pos)`: Returns line/column/square neighbors for any position
- `solve_sudoku()`: Main solving loop applying different strategies
- `cursedoku()`: Backtracking solver for puzzles requiring guessing

## Input Format

Text files with 9x9 grid where:
- Numbers 1-9 represent filled cells
- `*` represents empty cells
- Example files in `samples/` directory