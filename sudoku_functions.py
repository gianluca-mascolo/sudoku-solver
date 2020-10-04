#!/usr/bin/env python3

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
