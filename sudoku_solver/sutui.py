#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Static


class SudokuCell(Static):
    """Display Sudoku cell."""

    # def __init__(self, *args, **kwargs):
    #     self.id=1
    #     self.name="xx"
    # #pos = self.id
    # #pos = name
    DEFAULT_CSS = """
    SudokuCell {{
        height: {0};
    }}
    """.format(
        "1"
    )

    def on_mount(self) -> None:
        self.render()


class SudokuApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        for x in range(2):
            yield SudokuCell(id=f"cell{x}", renderable="X", name=f"{x}")


def main():
    app = SudokuApp()
    app.run()
    return True


if __name__ == "__main__":
    main()
