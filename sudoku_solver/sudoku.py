#!/usr/bin/python3
class SudokuBoard:
    def __init__(self):
        self.cell = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        self.board = [self.cell for x in range(81)]

    def full(self):
        board_len = sum(list(map(lambda x: len(x), self.board)))
        return board_len == 81

    def valid(self):
        for pos, element in enumerate(self.board):
            if element == set():
                print("Cell is empty")
                return False
            if element.issubset(self.cell) is False:
                print("Invalid cell content: {0}".format(element))
                return False
            if len(element) == 1:
                for x in range(9 * (pos // 9), 9 * (pos // 9) + 9):
                    if x != pos:
                        if self.board[x] == element:
                            print(
                                "Duplicate in line. Board {0} and Board {1} equal {2}".format(
                                    x, pos, element
                                )
                            )
                            return False
                for x in range(pos % 9, 81, 9):
                    if x != pos:
                        if self.board[x] == element:
                            print(
                                "Duplicate in Column. Board {0} and Board {1} equal {2}".format(
                                    x, pos, element
                                )
                            )
                            return False
                for x in range(81):
                    if (
                        3 * (x // 9 // 3) + x // 3 % 3
                        == 3 * (pos // 9 // 3) + pos // 3 % 3
                    ):
                        if x != pos:
                            if self.board[x] == element:
                                print(
                                    "Duplicate in Square. Board {0} and Board {1} equal {2}".format(
                                        x, pos, element
                                    )
                                )
                                return False
        return True


def load_sudoku(sudoku_file: str, sudoku: SudokuBoard):
    y = 0
    with open(sudoku_file, "r") as f:
        for line in f:
            for x in range(9):
                if line[x] != "*":
                    sudoku.board[y][x] = {line[x]}
            y += 1
    f.closed
    return sudoku.valid()


def main():
    sudoku = SudokuBoard()
    sudoku.board[0] = {"3"}
    sudoku.board[9] = {"3"}
    # print(sudoku.full())
    print(sudoku.valid())


if __name__ == "__main__":
    main()


# for x in range(81):
#    print("x: {0} r: {1}, q: {2} t: {3}".format(x,x//9//3,x//3%3,3*(x//9//3)+x//3%3))
