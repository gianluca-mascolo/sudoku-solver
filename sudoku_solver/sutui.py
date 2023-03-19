#!/usr/bin/env python3
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class SudokuCell(Static):
    """Display Sudoku cell."""

    def on_mount(self) -> None:
        self.render()


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
    """
    BINDINGS = [("s,S", "solve", "Solve"), ("c,C", "clear", "Clear"), ("q,Q", "quit", "Quit")]
    board = list(map(lambda x: x % 9 + 1, range(81)))
    position = 0
    sudoku_grid = [SudokuCell(id=f"cell{p}", renderable=f"{v}", name=f"{p}", classes="cell") for p, v in enumerate(board)]
    sudoku_grid[0].add_class("selected")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

        for p in range(81):
            yield self.sudoku_grid[p]
        yield Static("", classes="cell", id="filler")

    def on_key(self, event: events.Key) -> None:
        key = event.key
        p = self.position
        board = self.board
        if key in list(map(lambda c: str(c), range(1, 9))):
            board[p] = key
        else:
            board[p] = ""
        self.sudoku_grid[p].remove_class("selected")
        self.sudoku_grid[p].update(board[p])
        self.position = (p + 1) % 81
        self.sudoku_grid[self.position].add_class("selected")
        return True

    def action_quit(self) -> None:
        self.app.exit()

    def action_solve(self) -> None:
        return True

    def action_clear(self) -> None:
        return True


def main():
    app = SudokuApp()
    app.run()
    return True


if __name__ == "__main__":
    main()
