#!/usr/bin/env python3
import argparse
import copy
from functools import reduce
from itertools import combinations


class SudokuBoard:
    def __init__(self):
        self.board = [{"1", "2", "3", "4", "5", "6", "7", "8", "9"} for x in range(81)]

    def length(self) -> int:
        return len(list(filter(lambda x: len(x) == 1, self.board)))

    def valid(self) -> bool:
        for pos, element in enumerate(self.board):
            if element == set():
                # print("Cell is empty at Board {0}".format(pos))
                return False
            if element.issubset({"1", "2", "3", "4", "5", "6", "7", "8", "9"}) is False:
                # print("Invalid cell. position: {0} content: {1}".format(pos, element))
                return False
            if len(element) == 1:
                if element in [self.board[x] for x in neighbor(pos=pos)["all"]]:
                    # print("Find duplicate {0}".format(element))
                    return False
        return True

    def clear(self) -> None:
        self.board = [{"1", "2", "3", "4", "5", "6", "7", "8", "9"} for x in range(81)]


def load_sudoku(sudoku_file: str, sudoku: SudokuBoard) -> bool:
    try:
        with open(sudoku_file, "r") as f:
            for pos, c in enumerate(f.read()):
                if pos - pos // 10 < 81 and c in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                    sudoku.board[pos - pos // 10] = {c}
        f.closed
    except IOError as e:
        print(f"Input file error: {e}")
        return False
    if sudoku.length() == 0:
        print("Malformed input file")
        return False
    if sudoku.valid() is False:
        print("Sudoku is not valid in input file")
        return False
    return sudoku.valid()


def neighbor(pos: int, match=None) -> bool:
    line = [x for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
    column = [x for x in range(pos % 9, 81, 9) if x != pos]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
    if match is None:
        return {
            "line": line,
            "column": column,
            "square": square,
            "all": list(set(line + column + square)),
        }
    else:
        return {
            "line": [x for x in line if set(match).issubset(set(line)) and x not in set(match)],
            "column": [x for x in column if set(match).issubset(set(column)) and x not in set(match)],
            "square": [x for x in square if set(match).issubset(set(square)) and x not in set(match)],
            "all": [],
        }


def print_sudoku(sudoku: SudokuBoard) -> bool:
    print("+---+---+---+")
    for p in range(81):
        if p % 3 == 0:
            if p % 9 == 0 and p != 0:
                print("|")
                if p % 27 == 0 and p != 0:
                    print("+---+---+---+")
                print("|", end="")
            else:
                print("|", end="")
        if len(sudoku.board[p]) == 1:
            print(str(next(iter(sudoku.board[p]))), end="")
        else:
            print("_", end="")
    print("|")
    print("+---+---+---+")

    return True


# Different solving rules can be found at:
# https://sudoku.com/sudoku-rules/
def solve_sudoku(sudoku: SudokuBoard) -> bool:
    # print("solving sudoku")
    checked = set()
    while sudoku.valid() and sudoku.length() < 81 and sudoku.length() > len(checked):
        # print(f"sudoku len: {sudoku.length()}")
        # Every cell that contain only one number must be eliminated from its neighbors
        for position, element in filter(lambda x: len(x[1]) == 1, enumerate(sudoku.board)):
            for p in neighbor(position)["all"]:
                sudoku.board[p] -= element
                checked.add(position)
        # For every cell that contains more than one number...
        for position, element in filter(lambda x: len(x[1]) > 1, enumerate(sudoku.board)):
            for group in ["line", "square", "column"]:
                # ... if that number it's not present on any neighbor, than it must be in that cell.
                # https://sudoku.com/sudoku-rules/hidden-singles/
                if alone := element - reduce(lambda a, b: a | b, map(lambda x: sudoku.board[x], neighbor(position)[group])):
                    sudoku.board[position] = alone
        # https://sudoku.com/sudoku-rules/obvious-pairs/
        # For every cell that contains pair...
        for position, element in (twins := list(filter(lambda x: len(x[1]) == 2, enumerate(sudoku.board)))):
            twins_position = set([x[0] for x in twins if x[1] == element])  # ... get position of all pairs that math cell ...
            for combo in combinations(twins_position, 2):  # ... combine all position of my pairs in couples ...
                for group in ["line", "square", "column"]:
                    for p in neighbor(pos=combo[0], match=[combo[1]])[group]:  # ... all pair couples that are neighbors ...
                        sudoku.board[p].difference_update(element)  # ... must be eliminated from all other cells in neighborhood.
        # print_sudoku(sudoku)
    return sudoku.valid()


def cursedoku(sudoku: SudokuBoard, depth=0) -> bool:
    if sudoku.valid():
        if sudoku.length() == 81:
            return True
        elif sudoku.length() < 21:
            return False
        else:
            if depth < 3:  # Try to guess a maximum of 3 elements
                # print(f"*** recurse sudoku, depth: {depth}")
                unknowns = list(filter(lambda x: len(x[1]) > 1, enumerate(sudoku.board)))
                unknowns.sort(key=lambda x: len(x[1]))
                for position, element in unknowns:
                    trydoku = copy.deepcopy(sudoku.board)
                    for v in element:
                        # print(f"try value: {v} at position {position}")
                        sudoku.board[position] = {v}
                        solve_sudoku(sudoku)
                        if not cursedoku(sudoku, depth=depth + 1):
                            sudoku.board = copy.deepcopy(trydoku)
                            if depth > 1:  # fail fast: if the 3rd element is wrong, return false and change the 2nd
                                return False
                        else:
                            return True
            else:
                return False
    else:
        return False


def main():
    parser = argparse.ArgumentParser(prog="sudoku", description="Solve sudoku")
    parser.add_argument("-s", "--sudoku-file", help="Path to sudoku input file", type=str, required=True)
    args = parser.parse_args()
    sudoku = SudokuBoard()
    if load_sudoku(args.sudoku_file, sudoku):
        print_sudoku(sudoku)
        solve_sudoku(sudoku)
        cursedoku(sudoku)
        print(f"Sudoku is valid: {sudoku.valid()}")
        print_sudoku(sudoku)


if __name__ == "__main__":
    main()
