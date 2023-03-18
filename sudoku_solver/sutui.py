#!/usr/bin/env python3
from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget


class SudokuCell(Widget):
    """Display a sudoku input cell."""

    def render(self) -> RenderResult:
        return "[b]X[/b]"


class SudokuApp(App):
    def compose(self) -> ComposeResult:
        yield SudokuCell()


def main():
    app = SudokuApp()
    app.run()
    return True


if __name__ == "__main__":
    main()
