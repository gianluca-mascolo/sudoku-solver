#!/usr/bin/env python3

import sudoku_functions
from sudoku_functions import printSudoku,rawSudoku,loadSudoku,writeSudoku,digSudoku,checkSudoku,findUnique,findTwins



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

visited=[]
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

oldProgress=-1
Progress=0
newUnique=1
while Progress < 81 and newUnique > 0:
    while oldProgress < Progress:
        oldProgress=Progress
        for y in range(9):
            for x in range(9):
                if len(S[y][x])==1 and (x,y) not in visited:
                    S=digSudoku(S,x,y)
                    visited.append((x,y))
    newUnique=0
    for y in range(9):
        for x in range(9):
            if len(S[y][x])>1:
                S,changedS=findUnique(S,x,y)
                if changedS:
                    newUnique+=1
    printSudoku(S)
    Progress=len(visited)
    print("Got " + str(Progress) + " numbers." + "New Unique to explore: " + str(newUnique))

validSudoku,fullSudoku=checkSudoku(S)
if validSudoku:
    if fullSudoku:
        print("Sudoku completed")
    else:
        print("Sudoku is valid")
        rawSudoku(S)
        twins=findTwins(S)
        for t in twins:
            xt=t[0]
            yt=t[1]
            print(t,xt,yt,S[yt][xt])
            
    writeSudoku('sol.txt',S)
else:
    print("Error solving sudoku")
    exit(1)
