# coding: utf-8
# -----------------------------------------------------------------

import numpy as np
from random import choice, random

# -----------------------------------------------------------------


class MainGame():       

    def __init__(self,UNIT,H,W,EmptyStr):
        self.UNIT = UNIT
        self.H = H
        self.W = W
        self.EmptyStr = EmptyStr
        self.field = [[EmptyStr] * W for x in range(0,H)]
        self.score = 0


    def getFullIndex(self):
        return [[x, y] for x in range(self.H) for y in range(self.W)]
    
    def getEmptyIndex(self):
        return [[x, y] for x, y in self.getFullIndex() if self.field[x][y] == self.EmptyStr]

    def spawnNum(self):
        emptyList = self.getEmptyIndex()
        if emptyList:
            iX, iY = choice(emptyList)
            newNum = int(self.UNIT) if random() < 0.8 else int(self.UNIT) * 2
            self.field[iX][iY] = int(newNum)

    def anyEmpty(self):
        return np.any(np.array(self.field,dtype='U10') == self.EmptyStr)

    def showField(self):
        print(np.array(self.field,dtype='U10'))

    def moveLeftRight(self, iDir):
        np_field = np.array(self.field,dtype='U10')
        for x in range(self.H):
            oldL = list(np_field[x,:]) if iDir else list(np_field[x,::-1])
            newL = list(filter(lambda y: y != self.EmptyStr, oldL))
            newL = self.fusion(newL)
            if len(oldL) != len(newL):
                rept = len(oldL) - len(newL)
                addL = [self.EmptyStr] * rept 
                newL.extend(addL)
                newL = newL if iDir else list(reversed(newL))
                np_field[x,:] = newL[:]
                self.field = np_field.tolist()
            else:
                continue


    def moveUpDown(self, iDir):
        np_field = np.array(self.field,dtype='U10')
        for x in range(self.W):
            oldL = list(np_field[:,x]) if iDir else list(np_field[::-1,x])
            newL = list(filter(lambda y: y != self.EmptyStr, oldL))
            newL = self.fusion(newL)
            if len(oldL) != len(newL):
                rept = len(oldL) - len(newL)
                addL = [self.EmptyStr] * rept 
                newL.extend(addL)
                newL = newL if iDir else list(reversed(newL))
                np_field[:,x] = newL[:]
                self.field = np_field.tolist()
            else:
                continue    
                
    def fusion(self, subLine):
        tgtLine = subLine[:]
        N = len(tgtLine)
        for x in range(N-1):
            if tgtLine[x] != self.EmptyStr and tgtLine[x] == tgtLine[x+1]:
                fuVal = int(tgtLine[x]) * 2
                tgtLine[x] = fuVal
                self.score = self.score + fuVal
                del tgtLine[x+1]
                return tgtLine
        return tgtLine

    def fusionCheck(self):
        np_field = np.array(self.field,dtype='U10')        
        for x in range(self.W):
            testLine = list(np_field[:,x])
            for y in range(self.H-1):
                if testLine[y] == testLine[y+1]:
                    return True 
        for x in range(self.H):
            testLine = list(np_field[x,:])
            for y in range(self.W-1):
                if testLine[y] == testLine[y+1]:
                    return True 
        return False    

    def checkAlive(self):
        if self.anyEmpty():
            return True
        else:
            return True if self.fusionCheck() else False

# -----------------------------------------------------------------

def pickMove():
    
    A = True if random() <= 0.5 else False
    B = True if random() <= 0.5 else False
    
    if A:
        game.moveLeftRight(True) if B else game.moveLeftRight(False)
    else:
        game.moveUpDown(True) if B else game.moveUpDown(False)


# -----------------------------------------------------------------


UNIT = 2
H, W = 4, 4
EmptyStr = "-"

game = MainGame(UNIT,H,W,EmptyStr)

for _ in range(300):
    game.spawnNum()
    if game.checkAlive():
        pickMove()
    else:
        print("DEAD at: move -",_," / SCORE:", game.score)
        break

game.showField()


