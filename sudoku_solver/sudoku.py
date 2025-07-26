#!/usr/bin/env python3
import os
import sys

from textual import events
from textual.app import App, ComposeResult
from textual.screen import ModalScreen, Screen
from textual.validation import Function
from textual.widgets import DirectoryTree, Footer, Header, Input, Static

from sudoku_solver.sudokulib import SudokuBoard, cursedoku, load_sudoku, solve_sudoku  # NOQA

position = 0
sudoku_grid = []


class SudokuFile(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Return")]

    def __init__(self, sudoku: SudokuBoard):
        self.sudoku = sudoku
        super().__init__()

    def compose(self) -> ComposeResult:
        yield DirectoryTree("./samples/", classes="cell", id="loader")

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        event.stop()
        self.sudoku.clear()
        if load_sudoku(str(event.path), self.sudoku):
            for p, v in enumerate(self.sudoku.board):
                if len(v) == 1:
                    sudoku_grid[p].update(str(list(v)[0]))
                else:
                    sudoku_grid[p].update("")
        else:
            self.sudoku.clear()
            for p in range(81):
                sudoku_grid[p].update("")
        self.app.pop_screen()
        return None


class SaveFile(ModalScreen):
    CSS = """
    SaveFile {
        align: center middle;
        layout: vertical;
    }

    .box {
        height: auto;
        width: auto;
    }
    """

    BINDINGS = [("escape", "app.pop_screen", "Cancel")]

    def __init__(self, sudoku: SudokuBoard):
        self.sudoku = sudoku
        super().__init__()

    def on_input_submitted(self, event: Input.Submitted):
        if event.validation_result.is_valid:
            self.save_sudoku(event.value)
            self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter filename (without .txt)", classes="box", id="input", validators=[Function(self.validate_filename, "Invalid filename or file already exists")])
        yield Footer()

    def validate_filename(self, value: str) -> bool:
        if not value or "/" in value or "\\" in value:
            return False
        filepath = os.path.join("samples", f"{value}.txt")
        return not os.path.exists(filepath)

    def save_sudoku(self, filename: str) -> None:
        filepath = os.path.join("samples", f"{filename}.txt")
        with open(filepath, "w") as f:
            for i in range(81):
                if len(self.sudoku.board[i]) == 1:
                    f.write(str(list(self.sudoku.board[i])[0]))
                else:
                    f.write("*")
                if (i + 1) % 9 == 0:
                    f.write("\n")


class SudokuCell(Static):
    """Display Sudoku cell."""

    def on_mount(self) -> None:
        self.render()

    def on_click(self) -> None:
        global sudoku_grid
        global position
        sudoku_grid[position].remove_class("selected")
        self.add_class("selected")
        position = int(self.name)


class SudokuApp(App):
    CSS = """
    Screen {
        align: left top;
        layout: grid;
        grid-size: 9 11;
        grid-gutter: 0 0;
        grid-rows: 2;
        grid-columns: 3;
        padding: 0;
    }
    .cell {
    height: 2;
    width: 3;
    border-left: solid blue;
    border-top: solid blue;
    }
    .selected {
    height: 2;
    width: 3;
    border-left: solid yellow;
    border-top: solid yellow;
    }
    #filler {
    column-span: 9;
    row-span: 2;
    height: 100%;
    width: 100%;
    content-align: center middle;
    border: none
    }
    #loader {
    row-span: 9;
    column-span: 9;
    content-align: center middle;
    width: 100%;
    height: 100%;
    }
    """
    BINDINGS = [("s,S", "solve", "Solve"), ("c,C", "clear", "Clear"), ("l,L", "load_file", "Load"), ("w,W", "save_file", "Save"), ("q,Q", "quit", "Quit")]
    sudoku = SudokuBoard()

    for p, v in enumerate(sudoku.board):
        if len(v) == 1:
            sudoku_grid.append(SudokuCell(f"{list(v)[0]}", id=f"cell{p}", name=f"{p}", classes="cell"))
        else:
            sudoku_grid.append(SudokuCell("", id=f"cell{p}", name=f"{p}", classes="cell"))
    sudoku_grid[0].add_class("selected")
    message = Static("'1-9' insert, 'x' delete", classes="cell", id="filler")

    def compose(self) -> ComposeResult:
        global sudoku_grid
        yield Header(show_clock=True)
        yield Footer()

        for p in range(81):
            yield sudoku_grid[p]
        yield self.message

    def on_key(self, event: events.Key) -> None:
        global sudoku_grid
        global position
        key = event.key
        currentvalue = self.sudoku.board[position]
        sudoku_grid[position].remove_class("selected")
        if key in list(map(lambda c: str(c), range(1, 10))):
            self.sudoku.board[position] = {key}
            if self.sudoku.valid():
                sudoku_grid[position].update(key)
                position = (position + 1) % 81
            else:
                self.sudoku.board[position] = currentvalue
        elif key == "x" or key == "X":
            self.sudoku.board[position] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
            sudoku_grid[position].update("")
            position = (position + 1) % 81
        sudoku_grid[position].add_class("selected")

    def action_quit(self) -> None:
        self.app.exit(return_code=0)

    def action_solve(self) -> None:
        global sudoku_grid
        solve_sudoku(self.sudoku)
        cursedoku(self.sudoku)
        for p, v in enumerate(self.sudoku.board):
            if len(v) == 1:
                sudoku_grid[p].update(str(list(v)[0]))
            else:
                sudoku_grid[p].update("")

    def action_clear(self) -> None:
        global sudoku_grid
        global position
        for x in range(81):
            self.sudoku.board[x] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
            sudoku_grid[x].update("")
        sudoku_grid[position].remove_class("selected")
        position = 0
        sudoku_grid[0].add_class("selected")
        self.message.update("'1-9' insert, 'x' delete")

    def action_load_file(self) -> None:
        self.push_screen(SudokuFile(self.sudoku))

    def action_save_file(self) -> None:
        self.push_screen(SaveFile(self.sudoku))


def main():
    app = SudokuApp()
    exit_code = app.run()
    sys.exit(exit_code if exit_code is not None else 0)


if __name__ == "__main__":
    main()
