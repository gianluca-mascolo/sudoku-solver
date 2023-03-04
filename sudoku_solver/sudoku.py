#!/usr/bin/python3
class SudokuBoard:
    def __init__(self):
        cell = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        self.board = [
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
            [cell, cell, cell, cell, cell, cell, cell, cell, cell],
        ]

    def valid(self):
        for y in range(9):
            for x in range(9):
                print(self.board[y][x])
        return True


def main():
    sudoku = SudokuBoard()
    print(sudoku.valid())
    print("main")


if __name__ == "__main__":
    main()
