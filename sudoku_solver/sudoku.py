#!/usr/bin/python3
# import copy
from functools import reduce
from itertools import combinations


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
            if len(element) == 1:
                if element in [self.board[x] for x in neighbor(pos=pos)["all"]]:
                    print("Find duplicate {0}".format(element))
                    return False
        return True

    def list_elements(self, multiple):
        if multiple:
            return [{"position": x, "element": self.board[x]} for x in range(81) if len(self.board[x]) > 1]
        else:
            return [{"position": x, "element": self.board[x]} for x in range(81) if len(self.board[x]) == 1]

    def list_twins(self, exclude=[]):
        twins = []
        twins_checked = set()
        for pos in range(81):
            if len(self.board[pos]) == 2:
                for x in neighbor(pos=pos)["all"]:
                    if self.board[pos] == self.board[x] and x not in twins_checked:
                        twins.append({"position": [pos, x], "element": self.board[pos]})
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


def neighbor(pos: int):
    line = [x for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
    column = [x for x in range(pos % 9, 81, 9) if x != pos]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
    return {
        "line": line,
        "column": column,
        "square": square,
        "all": list(set(line + column + square)),
    }
    # return {
    #     "line": [x for x in line if x not in exclude],
    #     "column": [x for x in column if x not in exclude],
    #     "square": [x for x in square if x not in exclude],
    #     "all": list(set(line + column + square) - set(exclude)),
    # }


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
    while sudoku.valid() and sudoku.full() is False and len(sudoku.list_elements(multiple=False)) > len(checked):
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
                for p in twin_neighbor(combo[0], combo[1]):
                    sudoku.board[p].difference_update(element)
        print_sudoku(sudoku)
    return sudoku.valid()


def main():
    sudoku = SudokuBoard()
    load_sudoku("sudoku2.txt", sudoku)
    print_sudoku(sudoku)
    solve_sudoku(sudoku)
    print(sudoku.valid())
    for v in [{"position": x, "element": sudoku.board[x]} for x in range(81) if len(sudoku.board[x]) > 1]:
        print(v)
    # while sudoku.valid() and sudoku.full() is False:
    #     for twin in sudoku.list_twins():
    #         for v in twin["value"]:
    #             trydoku = copy.deepcopy(sudoku.board)
    #             sudoku.board[twin["position"][0]] = {v}
    #             r = solve_sudoku(sudoku)
    #             if r is False:
    #                 sudoku.board = copy.deepcopy(trydoku)
    #                 print(sudoku.board[twin["position"][0]])
    #                 print(f"Try: {r}")
    #         print(f"sudoku is valid: {sudoku.valid()}")
    #         print_sudoku(sudoku)


if __name__ == "__main__":
    main()
