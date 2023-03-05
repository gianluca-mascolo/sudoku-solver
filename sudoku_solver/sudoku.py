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

    def unique(self):
        return [x for x in range(81) if len(self.board[x]) == 1]


class SudokuChecklist:
    def __init__(self):
        self.checklist = [{"checked": False, "unique": False, "value": ""} for x in range(81)]


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


def neighbor(pos: int, unique=[]):
    line = [x for x in range(9 * (pos // 9), 9 * (pos // 9) + 9) if x != pos]
    column = [x for x in range(pos % 9, 81, 9) if x != pos]
    square = [x for x in range(81) if 3 * (x // 9 // 3) + x // 3 % 3 == 3 * (pos // 9 // 3) + pos // 3 % 3 and x != pos]
    return list(set(line + column + square) - set(unique))


def main():
    sudoku = SudokuBoard()
    load_sudoku("sudoku1.txt", sudoku)
    print(sudoku.valid())
    control = SudokuChecklist()
    for x in sudoku.unique():
        control.checklist[x]["unique"] = True
        control.checklist[x]["value"] = str(next(iter(sudoku.board[x])))

    # for x in control.checklist:
    #     print(f"{x['checked']} {x['unique']} {x['value']}")
    # print(sudoku.board)
    # board_len = sum(list(map(lambda x: len(x), self.board)))
    totunique = sum(list(map(lambda x: x["unique"], control.checklist)))
    print(f"tot: {totunique}")
    for pos, x in enumerate(control.checklist):
        if x["unique"] is True and x["checked"] is False:
            # print(neighbor(pos))
            for p in neighbor(pos, unique=sudoku.unique()):
                print(
                    f"Operation * value position: {pos} delete value: {x['value']} sudoku cell: {p} sudoku content: {sudoku.board[p]} cell len: {len(sudoku.board[p])} sudoku valid: {sudoku.valid()}"
                )
                sudoku.board[p].discard(x["value"])
                if len(sudoku.board[p]) == 1:
                    control.checklist[p]["unique"] = True
                    control.checklist[p]["value"] = str(next(iter(sudoku.board[p])))
                print(f"Result * value position: {pos} delete value: {x['value']} sudoku cell: {p} sudoku content: {sudoku.board[p]} cell len: {len(sudoku.board[p])} sudoku valid: {sudoku.valid()}")
                control.checklist[pos]["checked"] = True
    totunique = sum(list(map(lambda x: x["unique"], control.checklist)))
    print(f"tot: {totunique}")
    # print(sudoku.board)
    # print(sudoku.unique())
    # print(neighbor(0))
    # sudoku.board[1] = {"1"}
    # sudoku.board[9] = {"1"}

    # print(sudoku.full())
    # print(sudoku.valid())


if __name__ == "__main__":
    main()


# for x in range(81):
#    print("x: {0} r: {1}, q: {2} t: {3}".format(x,x//9//3,x//3%3,3*(x//9//3)+x//3%3))
