# Python Sudoku Solver

Try to solve sudokus with python

## Howto use

Write an input file called s.txt (or link s.txt to an input file with any name) then execute
`./sudoku.py`
Sudoku solution will be written in the same input format to `sol.txt`
## Input file format

Text file representing  a 9x9 square. Write a number per square, empty cells are marked with a `*` sign. See examples in repo.

## Demo

With example file `sudoku2.txt`

```
3***67*5*
*81**5**9
*6**8*1**
*******93
1*4***5*6
69*******
**8*1**4*
9**5**86*
*5*97***1
```
You get the following solutions.
```
+---+---+---+
|349|167|258|
|281|435|679|
|567|289|134|
+---+---+---+
|872|651|493|
|134|792|586|
|695|843|712|
+---+---+---+
|728|316|945|
|913|524|867|
|456|978|321|
+---+---+---+
```
## Notes
Not all sudokus solve completely