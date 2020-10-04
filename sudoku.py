#!/usr/bin/env python3

import sudoku_functions
from sudoku_functions import printSudoku,rawSudoku,loadSudoku,writeSudoku,checkSudoku,solveDoku

S=[
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()],
   [set(),set(),set(),set(),set(),set(),set(),set(),set()]
  ]

S=loadSudoku('s.txt',S)
validSudoku,fullSudoku=checkSudoku(S)
if validSudoku:
    if fullSudoku:
        print("Sudoku completed")
        printSudoku(S)
        exit(0)
    else:
        print("Solving Sudoku")
else:
    print("Input file not valid")
    exit(1)

validSudoku,S=solveDoku(S)
if validSudoku:
    writeSudoku('sol.txt',S)
else:
    print("Error solving sudoku")
    rawSudoku(S)
