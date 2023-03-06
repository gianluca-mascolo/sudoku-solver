#!/usr/bin/python3
import copy
from enum import Enum


class SudokuGroup(Enum):
    LINE, COLUMN, SQUARE, ALL = range(4)


class SudokuBoard:
    def __init__(self):
        self.board = [{"1", "2", "3", "4", "5", "6", "7", "8", "9"} for x in range(81)]

    def full(self):
        board_len = sum(list(map(lambda x: len(x), self.board)))
        return board_len == 81

    def valid(self):
        for pos, element in enumerate(self.board):
            if element == set():
                print("Cell is empty at Board {0}".format(pos))
                return False
            if element.issubset({"1", "2", "3", "4", "5", "6", "7", "8", "9"}) is False:
                print("Invalid cell. position: {0} content: {1}".format(pos, element))
                return False
            if self.is_unique(pos):
                if element in [self.board[x] for x in neighbor(pos=pos, group=SudokuGroup.ALL)]:
                    print("Find duplicate {0}".format(element))
                    return False
        return True

    def list_unique(self, exclude=[]):
        return [x for x in range(81) if len(self.board[x]) == 1 and x not in exclude]

    def list_multiple(self, exclude=[]):
        return [x for x in range(81) if len(self.board[x]) > 1 and x not in exclude]

    def is_unique(self, pos: int):
        if len(self.board[pos]) == 1:
            return str(next(iter(self.board[pos])))
        else:
            return False

    def list_twins(self, exclude=[]):
        twins = []
        twins_checked = set()
        for pos in range(81):
            if len(self.board[pos]) == 2:
                for x in neighbor(pos=pos, group=SudokuGroup.ALL):
                    if self.board[pos] == self.board[x] and x not in twins_checked:
                        twins.append({"position": [pos, x], "value": self.board[pos]})
                        twins_checked.add(pos)
                        twins_checked.add(x)
        return twins


def load_sudoku(sudoku_file: str, sudoku: SudokuBoard):
    with open(sudoku_file, "r") as f:
        for pos, c in enumerate(f.read()):
            if pos - pos // 10 < 81 and c in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                sudoku.board[pos - pos // 10] = {c}
    f.closed
    return sudoku.valid()


def neighbor(pos: int, group: SudokuGroup, exclude=[]):
    line = [x for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
    column = [x for x in range(pos % 9, 81, 9) if x != pos]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
    if group == SudokuGroup.ALL:
        return list(set(line + column + square) - set(exclude))
    elif group == SudokuGroup.LINE:
        return line
    elif group == SudokuGroup.COLUMN:
        return column
    elif group == SudokuGroup.SQUARE:
        return square


def twin_neighbor(t1: int, t2: int):
    line = [x for x in range(9 * (t1 // 9), 9 * (t1 // 9) + 9) if x != t1]
    column = [x for x in range(t1 % 9, 81, 9) if x != t1]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (t1 // 9 // 3) + t1 // 3 % 3 and x != t1]
    if t2 in line:
        return list(set(line) - set([t2]))
    elif t2 in column:
        return list(set(column) - set([t2]))
    elif t2 in square:
        return list(set(square) - set([t2]))
    else:
        return []


def print_sudoku(sudoku: SudokuBoard):
    unique = sudoku.list_unique()
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
        if p in unique:
            print(str(next(iter(sudoku.board[p]))), end="")
        else:
            print("_", end="")
    print("|")
    print("+---+---+---+")

    return True


def solve_sudoku(sudoku: SudokuBoard):
    print("solving sudoku")
    checked = set()
    while sudoku.valid() and sudoku.full() is False and len(sudoku.list_unique()) > len(checked):
        print(f"Total unique: {len(sudoku.list_unique())} {len(checked)}")
        for x in sudoku.list_unique(exclude=list(checked)):
            for p in neighbor(pos=x, group=SudokuGroup.ALL, exclude=sudoku.list_unique()):
                sudoku.board[p].discard(sudoku.is_unique(x))
                checked.add(x)
        for x in sudoku.list_multiple():
            for v in sudoku.board[x]:
                if sum(list(map(lambda i: v not in sudoku.board[i], neighbor(x, SudokuGroup.LINE)))) == 8:
                    sudoku.board[x] = {v}
                if sum(list(map(lambda i: v not in sudoku.board[i], neighbor(x, SudokuGroup.COLUMN)))) == 8:
                    sudoku.board[x] = {v}
                if sum(list(map(lambda i: v not in sudoku.board[i], neighbor(x, SudokuGroup.SQUARE)))) == 8:
                    sudoku.board[x] = {v}
        for twin in sudoku.list_twins():
            for p in twin_neighbor(twin["position"][0], twin["position"][1]):
                sudoku.board[p].difference_update(twin["value"])
        print_sudoku(sudoku)
    return sudoku.valid()


def main():
    sudoku = SudokuBoard()
    load_sudoku("sudoku2.txt", sudoku)
    solve_sudoku(sudoku)
    while sudoku.valid() and sudoku.full() is False:
        for twin in sudoku.list_twins():
            for v in twin["value"]:
                trydoku = copy.deepcopy(sudoku.board)
                sudoku.board[twin["position"][0]] = {v}
                r = solve_sudoku(sudoku)
                if r is False:
                    sudoku.board = copy.deepcopy(trydoku)
                    print(sudoku.board[twin["position"][0]])
                    print(f"Try: {r}")
            print(f"sudoku is valid: {sudoku.valid()}")
            print_sudoku(sudoku)


if __name__ == "__main__":
    main()
