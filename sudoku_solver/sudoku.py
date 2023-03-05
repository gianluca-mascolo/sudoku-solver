#!/usr/bin/python3
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
                line = [self.board[x] for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
                if element in line:
                    print("Duplicate in line")
                    return False
                column = [self.board[x] for x in range(pos % 9, 81, 9) if x != pos]
                if element in column:
                    print("Duplicate in column")
                    return False
                square = [self.board[x] for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
                if element in square:
                    print("Duplicate in square")
                    return False
        return True

    def list_unique(self, exclude=[]):
        return [x for x in range(81) if len(self.board[x]) == 1 and x not in exclude]

    def is_unique(self, pos: int):
        if len(self.board[pos]) == 1:
            return str(next(iter(self.board[pos])))
        else:
            return False


def load_sudoku(sudoku_file: str, sudoku: SudokuBoard):
    y = 0
    with open(sudoku_file, "r") as f:
        for line in f:
            for x in range(9):
                if line[x] != "*":
                    sudoku.board[y * 9 + x] = {line[x]}
            y += 1
    f.closed
    return sudoku.valid()


def neighbor(pos: int, exclude=[]):
    line = [x for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
    column = [x for x in range(pos % 9, 81, 9) if x != pos]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
    return list(set(line + column + square) - set(exclude))


def main():
    sudoku = SudokuBoard()
    load_sudoku("sudoku1.txt", sudoku)
    print(sudoku.valid())
    checked = set()
    while sudoku.valid() and sudoku.full() is False and len(sudoku.list_unique()) > len(checked):
        print(f"Total unique: {len(sudoku.list_unique())} {len(checked)} {len(sudoku.list_unique())}")
        for x in sudoku.list_unique(exclude=list(checked)):
            for p in neighbor(x, exclude=sudoku.list_unique()):
                sudoku.board[p].discard(sudoku.is_unique(x))
                checked.add(x)
        print(f"Total unique: {len(sudoku.list_unique())} {len(checked)} {len(sudoku.list_unique())}")
    print(sudoku.board)


if __name__ == "__main__":
    main()
