from sudoku_solver.sudoku import SudokuBoard, load_sudoku


def test_valid():
    sudoku = SudokuBoard()
    assert sudoku.valid() is True
    assert sudoku.full() is False
    sudoku.board[0][0] = {"1"}
    sudoku.board[0][1] = {"1"}
    assert sudoku.valid() is False
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
    assert sudoku.valid() is True
    assert sudoku.full() is True


def test_load():
    sudoku = SudokuBoard()
    r = load_sudoku("sudoku1.txt", sudoku)
    assert r
