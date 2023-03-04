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
                print(self.board[y][x])
        return True


def main():
    sudoku = SudokuBoard()
    print(sudoku.valid())
    print("main")


if __name__ == "__main__":
    main()
