#!/usr/bin/python3
class SudokuBoard:
    def __init__(self):
        self.cell = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        self.board = [
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
            [
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
                self.cell,
            ],
        ]

    def full(self):
        uniqueSets = 0
        for y in range(9):
            for x in range(9):
                if len(self.board[y][x]) == 1:
                    uniqueSets += 1
        if uniqueSets == 81:
            return True
        else:
            return False

    def valid(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == set():
                    print("set not found")
                    return False
                if str(next(iter(self.board[y][x]))) not in self.cell:
                    print("Invalid cell")
                    return False
                if len(self.board[y][x]) == 1:
                    for dx in range(9):
                        if dx != x and self.board[y][x] == self.board[y][dx]:
                            print("Duplicate in line")
                            return False
                    for dy in range(9):
                        if dy != y and self.board[y][x] == self.board[dy][x]:
                            print("Duplicate in column")
                            return False
                    for dy in range(y - y % 3, y + (3 - y % 3)):
                        for dx in range(x - x % 3, x + (3 - x % 3)):
                            if (dy != y or dx != x) and self.board[dy][
                                dx
                            ] == self.board[y][x]:
                                print("Duplicate in square")
                                return False
        return True


def main():
    sudoku = SudokuBoard()
    print("Is Valid: {0}".format(sudoku.valid()))
    print("Is Full: {0}".format(sudoku.full()))
    sudoku.board[0][0] = {"1"}
    sudoku.board[0][1] = {"1"}
    print("Is Valid: {0}".format(sudoku.valid()))
    print("Is Full: {0}".format(sudoku.full()))
    sudoku.board = [
        [{"3"}, {"4"}, {"9"}, {"1"}, {"6"}, {"7"}, {"2"}, {"5"}, {"8"}],
        [{"2"}, {"8"}, {"1"}, {"4"}, {"3"}, {"5"}, {"6"}, {"7"}, {"9"}],
        [{"5"}, {"6"}, {"7"}, {"2"}, {"8"}, {"9"}, {"1"}, {"3"}, {"4"}],
        [{"8"}, {"7"}, {"2"}, {"6"}, {"5"}, {"1"}, {"4"}, {"9"}, {"3"}],
        [{"1"}, {"3"}, {"4"}, {"7"}, {"9"}, {"2"}, {"5"}, {"8"}, {"6"}],
        [{"6"}, {"9"}, {"5"}, {"8"}, {"4"}, {"3"}, {"7"}, {"1"}, {"2"}],
        [{"7"}, {"2"}, {"8"}, {"3"}, {"1"}, {"6"}, {"9"}, {"4"}, {"5"}],
        [{"9"}, {"1"}, {"3"}, {"5"}, {"2"}, {"4"}, {"8"}, {"6"}, {"7"}],
        [{"4"}, {"5"}, {"6"}, {"9"}, {"7"}, {"8"}, {"3"}, {"2"}, {"1"}],
    ]
    print("Is Valid: {0}".format(sudoku.valid()))
    print("Is Full: {0}".format(sudoku.full()))


if __name__ == "__main__":
    main()
