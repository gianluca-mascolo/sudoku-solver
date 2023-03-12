#!/usr/bin/python3
import copy
from functools import reduce
from itertools import combinations


class SudokuBoard:
    def __init__(self):
        self.board = [{"1", "2", "3", "4", "5", "6", "7", "8", "9"} for x in range(81)]

    def length(self):
        return len(list(filter(lambda x: len(x) == 1, self.board)))

    def valid(self):
        for pos, element in enumerate(self.board):
            if element == set():
                print("Cell is empty at Board {0}".format(pos))
                return False
            if element.issubset({"1", "2", "3", "4", "5", "6", "7", "8", "9"}) is False:
                print("Invalid cell. position: {0} content: {1}".format(pos, element))
                return False
            if len(element) == 1:
                if element in [self.board[x] for x in neighbor(pos=pos)["all"]]:
                    print("Find duplicate {0}".format(element))
                    return False
        return True


def load_sudoku(sudoku_file: str, sudoku: SudokuBoard):
    with open(sudoku_file, "r") as f:
        for pos, c in enumerate(f.read()):
            if pos - pos // 10 < 81 and c in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                sudoku.board[pos - pos // 10] = {c}
    f.closed
    return sudoku.valid()


def neighbor(pos: int, match=None):
    line = [x for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
    column = [x for x in range(pos % 9, 81, 9) if x != pos]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
    if not match:
        return {
            "line": line,
            "column": column,
            "square": square,
            "all": list(set(line + column + square)),
        }
    else:
        return {
            "line": [x for x in line if match in line and x != match],
            "column": [x for x in column if match in column and x != match],
            "square": [x for x in square if match in square and x != match],
            "all": [],
        }


def print_sudoku(sudoku: SudokuBoard):
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


def solve_sudoku(sudoku: SudokuBoard):
    print("solving sudoku")
    checked = set()
    while sudoku.valid() and sudoku.length() < 81 and sudoku.length() > len(checked):
        print(f"sudoku len: {sudoku.length()}")
        for position, element in filter(lambda x: len(x[1]) == 1, enumerate(sudoku.board)):
            for p in neighbor(position)["all"]:
                sudoku.board[p] -= element
                checked.add(position)
        for position, element in filter(lambda x: len(x[1]) > 1, enumerate(sudoku.board)):
            for group in ["line", "square", "column"]:
                if alone := element - reduce(lambda a, b: a | b, map(lambda x: sudoku.board[x], neighbor(position)[group])):
                    sudoku.board[position] = alone
        for position, element in (twins := list(filter(lambda x: len(x[1]) == 2, enumerate(sudoku.board)))):
            twins_position = set([x[0] for x in twins if x[1] == element])
            for combo in combinations(twins_position, 2):
                for group in ["line", "square", "column"]:
                    for p in neighbor(pos=combo[0], match=combo[1])[group]:
                        sudoku.board[p].difference_update(element)
        print_sudoku(sudoku)
    return sudoku.valid()


def cursedoku(sudoku: SudokuBoard, depth=0):
    if sudoku.valid():
        if sudoku.length() == 81:
            return True
        else:
            if depth < 3:
                print(f"*** recurse sudoku, depth: {depth}")
                for position, element in filter(lambda x: len(x[1]) > 1, enumerate(sudoku.board)):
                    trydoku = copy.deepcopy(sudoku.board)
                    for v in element:
                        sudoku.board[position] = {v}
                        solve_sudoku(sudoku)
                        if not cursedoku(sudoku, depth=depth + 1):
                            sudoku.board = copy.deepcopy(trydoku)
                        else:
                            return True
            else:
                return False
    else:
        return False


def main():
    sudoku = SudokuBoard()
    load_sudoku("sudoku7.txt", sudoku)
    print_sudoku(sudoku)
    solve_sudoku(sudoku)
    cursedoku(sudoku)
    print(f"Sudoku is valid: {sudoku.valid()}")
    print_sudoku(sudoku)


if __name__ == "__main__":
    main()
