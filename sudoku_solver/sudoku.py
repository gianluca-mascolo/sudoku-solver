#!/usr/bin/env python3
from textual import events
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import DirectoryTree, Footer, Header, Static

from sudoku_solver.sudokulib import SudokuBoard, cursedoku, solve_sudoku

position = 0
sudoku_grid = []


class SudokuFile(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield DirectoryTree("./samples/", classes="cell", id="loader")


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
        # self.position=int(self.name)


class SudokuApp(App):
    CSS = """
    Screen {
        align: left top;
        layout: grid;
        grid-size: 9 10;
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
    BINDINGS = [("s,S", "solve", "Solve"), ("c,C", "clear", "Clear"), ("l,L", "push_screen('sudokufile')", "Load"), ("q,Q", "quit", "Quit")]
    SCREENS = {"sudokufile": SudokuFile()}
    sudoku = SudokuBoard()
    for p, v in enumerate(sudoku.board):
        if len(v) == 1:
            sudoku_grid.append(SudokuCell(id=f"cell{p}", renderable=f"{list(v)[0]}", name=f"{p}", classes="cell"))
        else:
            sudoku_grid.append(SudokuCell(id=f"cell{p}", renderable="", name=f"{p}", classes="cell"))
    sudoku_grid[0].add_class("selected")

    def compose(self) -> ComposeResult:
        global sudoku_grid
        yield Header(show_clock=True)
        yield Footer()

        for p in range(81):
            yield sudoku_grid[p]
        yield Static("", classes="cell", id="filler")

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
        self.app.exit()

    def action_solve(self) -> None:
        solve_sudoku(self.sudoku)
        cursedoku(self.sudoku)
        for p, v in enumerate(self.sudoku.board):
            if len(v) == 1:
                self.sudoku_grid[p].update(str(list(v)[0]))

    def action_clear(self) -> None:
        global sudoku_grid
        global position
        for x in range(81):
            self.sudoku.board[x] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
            self.sudoku_grid[x].update("")
        self.sudoku_grid[position].remove_class("selected")
        position = 0
        self.sudoku_grid[0].add_class("selected")

    def action_load(self) -> None:
        return None


def main():
    app = SudokuApp()
    app.run()
    return True


if __name__ == "__main__":
    main()
