#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Static


class SudokuCell(Static):
    """Display Sudoku cell."""

    def on_mount(self) -> None:
        self.render()


class SudokuApp(App):
    CSS = """
    Screen {
        align: left top;
        layout: grid;
        grid-size: 3 3;
        grid-gutter: 1;
        grid-rows: 1fr;
        grid-columns: 1fr;
    }
    .cell {
    height: 3;
    width: 3;
    border: solid green;
    }
    """
    board = list(range(9))

    def compose(self) -> ComposeResult:
        for p, v in enumerate(self.board):
            yield SudokuCell(id=f"cell{p}", renderable=f"{v}", name=f"{p}", classes="cell")


def main():
    app = SudokuApp()
    app.run()
    return True


if __name__ == "__main__":
    main()
