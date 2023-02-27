#!/usr/bin/env python3

import copy
def printSudoku(S):
    print('+---+---+---+')
    for y in range(9):
        print('|', end='')
        for x in range(9):
            if len(S[y][x])==1:
                print(next(iter(S[y][x])), end = '')
            else:
                print('_', end = '')
            if (x%3)==2:
                print('|', end='')
        print('')
        if (y%3)==2:
            print('+---+---+---+')

def rawSudoku(S):
    for y in range(9):
        print("l"+str(y+1)+": ",end='')
        for x in range(9):
            print(str(S[y][x])+" ", end = '')
            if (x%3)==2:
                print(' * ', end='')
        print('')

def loadSudoku(sudokuFile,S):
    y=0
    with open(sudokuFile,'r') as f:
        for line in f:
            for x in range(9):
                if line[x] != '*':
                    S[y][x]={line[x]}
                else:
                    S[y][x]={'1','2','3','4','5','6','7','8','9'}
            y+=1
    f.closed
    return S

def writeSudoku(sudokuFile,S):
    with open(sudokuFile,'w') as f:
        for y in range(9):
            for x in range(9):
                if len(S[y][x])==1:
                    f.write(next(iter(S[y][x])))
                else:
                    f.write('*')
            f.write('\n')
    f.closed
    
def digSudoku(S,x,y):
    seekValue = next(iter(S[y][x]))
    for dx in range(9):
        if dx != x:
            S[y][dx].discard(seekValue)
    for dy in range(9):
        if dy != y:
            S[dy][x].discard(seekValue)
    for dy in range(y-y%3,y+(3-y%3)):
        for dx in range(x-x%3,x+(3-x%3)):
            if dy !=y or dx != x:
                S[dy][dx].discard(seekValue)
    return S

def checkSudoku(S):
    uniqueSets=0
    for y in range(9):
        for x in range(9):
            if S[y][x] == set():
                return False,False
            if len(S[y][x])==1:
                uniqueSets+=1
                if str(next(iter(S[y][x]))) not in {'1','2','3','4','5','6','7','8','9'}:
                    return False,False
                for dx in range(9):
                    if dx != x and S[y][x]==S[y][dx]:
                        return False,False
                for dy in range(9):
                    if dy != y and S[y][x]==S[dy][x]:
                        return False,False
                for dy in range(y-y%3,y+(3-y%3)):
                    for dx in range(x-x%3,x+(3-x%3)):
                        if (dy !=y or dx != x) and S[dy][dx]==S[y][x]:
                            return False,False
    if uniqueSets==81:
        return True,True
    else:
        return True,False

def findUnique(S,x,y):
    originalS=S
    currentSet=S[y][x]
    leftSet=set()
    for dx in range(9):
        if dx != x:
            leftSet=leftSet.union(S[y][dx])
    if len(currentSet-leftSet)==1:
        S[y][x]=currentSet-leftSet
        if checkSudoku(S):
            return S,True
        else:
            return originalS,False
    leftSet=set()
    for dy in range(9):
        if dy != y:
            leftSet=leftSet.union(S[dy][x])
    if len(currentSet-leftSet)==1:
        S[y][x]=currentSet-leftSet
        if checkSudoku(S):
            return S,True
        else:
            return originalS,False
    leftSet=set()
    for dy in range(y-y%3,y+(3-y%3)):
        for dx in range(x-x%3,x+(3-x%3)):
            if dy !=y or dx != x:
                leftSet=leftSet.union(S[dy][dx])
    if len(currentSet-leftSet)==1:
        S[y][x]=currentSet-leftSet
        if checkSudoku(S):
            return S,True
        else:
            return originalS,False
    return originalS,False

def findTwins(S):
    twinsCoord=set()
    gotTwins=set()
    discardTwins=set()
    for y in range(9):
        for x in range(9):
            if len(S[y][x])==2:
                twinsCoord.add((x,y))
    for pivotCoord in twinsCoord:
        pivotX=pivotCoord[0]
        pivotY=pivotCoord[1]
        for checkCoord in twinsCoord:
            checkX=checkCoord[0]
            checkY=checkCoord[1]
            if (pivotX==checkX and not pivotY==checkY) or (pivotY==checkY and not pivotX==checkX) or ((checkX != pivotX and checkY!=pivotY) and (pivotX-pivotX%3 <= checkX < pivotX+(3-pivotX%3)) and (pivotY-pivotY%3 <= checkY < pivotY+(3-pivotY%3))):
                if S[pivotY][pivotX]==S[checkY][checkX] and (pivotX,pivotY) not in discardTwins:
                    gotTwins.add((pivotX,pivotY))
                    discardTwins.add((checkX,checkY))
    return(gotTwins)

def solveDoku(S):
    visited=[]
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
        if not fullSudoku:
            print("Sudoku is valid, checking twins")
            twins=findTwins(S)
            if len(twins)==0:
                print("No twins found")
                rawSudoku(S)
                printSudoku(S)
                print("Sudoku not completed")
            for t in twins:
                xt=t[0]
                yt=t[1]
                trySudoku=copy.deepcopy(S)
                for tryValue in S[yt][xt]:
                    trySudoku[yt][xt]={tryValue}
                    tryValid,trySudoku=solveDoku(trySudoku)
                    if tryValid:
                        return True,trySudoku
        else:
            print("Sudoku completed")
        return True,S
    else:
        print("Error solving sudoku")
        return False,S

