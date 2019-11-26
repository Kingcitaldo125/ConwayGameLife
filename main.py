import pygame
import random
import time
import sys

regularCells = []
topCells = []
bottomCells = []
leftCells = []
rightCells = []

allCells = []
aliveCells = []
deadCells = []

cellTypes = ["topLeftCorner", "topRightCorner", "bottomLeftCorner", "bottomRightCorner",
             "leftEdge", "rightEdge", "topEdge", "bottomEdge", "Regular"]


class Cell(object):
    def __init__(self, size, x, y, idx, cellType):
        global aliveCells, deadCells
        self.listIndex = idx
        self.x = x
        self.y = y
        self.w = size
        self.h = self.w
        self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        self.alive = False # dead
        ranLive = random.randrange(0, 12)
        if ranLive == 2:
            self.alive = True
            aliveCells.append(self)
        deadCells.append(self)
        self.mPos = 1
        self.type = cellType
        self.poisioned = False
        self.poisionedSteps = 0
        self.timesPoisioned = 0

        self.neighs = []

    def getNeighbors(self, numRows, numCols):
        global allCells, regularCells, topCells, bottomCells,\
        rightCells, leftCells, cellTypes, neighborOffsets, practiceList

        ns = []
        #print("NumRows:", numRows)
        #print("NumCols:", numCols)

        # Top
        for i in range(self.listIndex - (numCols+1), self.listIndex - (numCols-2)):
            if i > -1 and i < len(allCells)-1:
                ns.append(allCells[i])

        # Mid
        leftCell = self.listIndex - 1
        rightCell = self.listIndex + 1

        if leftCell > -1 and rightCell < len(allCells)-1:
            ns.append(allCells[leftCell])
            ns.append(allCells[rightCell])

        # Bottom
        for i in range(self.listIndex + (numCols-1), self.listIndex + (numCols+2)):
            if i > -1 and i < len(allCells):
                ns.append(allCells[i])

        #print(ns)
        self.neighs = ns
        return ns

    def decide(self, r, c):
        global aliveCells, deadCells
        # Conway's Game of Life.
        # GAME RULES:
        # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by over-population.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        self.getNeighbors(r, c)
        aliveNeighs = 0
        deadNeighs = 0
        poisionedNeighbors = 0
        swapped = False

        if self.timesPoisioned >= 4:
            if self.poisioned:
                self.alive = False
                self.poisioned = False
                if self in aliveCells:
                    aliveCells.remove(self)
                    deadCells.append(self)
                return swapped

        if self.poisioned:
            if self.poisionedSteps < 3:
                self.poisionedSteps += 1
            else:
                self.alive = False
                if self in aliveCells:
                    aliveCells.remove(self)
                    deadCells.append(self)
                self.poisionedSteps = 0
                return swapped

        # Get neighbors and their status
        for n in self.neighs:
            if n.poisioned:
                poisionedNeighbors += 1
            if n.alive:
                aliveNeighs += 1
            else:
                deadNeighs += 1

        if poisionedNeighbors == len(self.neighs):
            self.alive = False
            if self in aliveCells:
                aliveCells.remove(self)
                deadCells.append(self)
            return swapped

        if self.alive:
            if aliveNeighs < 2:
                self.alive = False
                if self in aliveCells:
                    aliveCells.remove(self)
                    deadCells.append(self)
                swapped = True
            elif aliveNeighs == 2 or aliveNeighs == 3:
                # Live on to next gen
                self.alive = True
            else:
                # If poisioned, infect neighbors
                if self.poisioned:
                    for n in self.neighs:
                        if not n.poisioned and n.alive:
                            n.poisioned = True
                    self.timesPoisioned += 1
                # Death by overcrowding.
                self.alive = False
                if self in aliveCells:
                    aliveCells.remove(self)
                    deadCells.append(self)
                swapped = True
        else:
            if aliveNeighs == 3:
                # Reproduce
                self.alive = True
                if self in deadCells:
                    deadCells.remove(self)
                    aliveCells.append(self)
                swapped = True
        return swapped

    def draw(self, surf, mPos, optionalcolor=(255, 255, 255)):
        #for n in self.neighs:
        #    pygame.draw.rect(surf, (20, 50, 100), (n.x, n.y, n.w, n.h))
        #pygame.draw.rect(surf, optionalcolor, (self.x, self.y, self.w, self.h))
        if self.alive:
            if self.poisioned:
                #print("POSIONED!!!!")
                pygame.draw.rect(surf, (0, 255, 0), (self.x, self.y, self.w, self.h))
            else:
                pygame.draw.rect(surf, (0, 0, 0), (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(surf, optionalcolor, (self.x, self.y, self.w, self.h))


def createCells(wx, wy, size):
    global cells, topCells, bottomCells,\
        rightCells, leftCells, allCells

    rows = int(wy / size) # screen width / cell size
    cols = int(wx / size) # screen height / cell size

    totalCells = rows * cols

    #print("Rows:", rows)
    #print("Columns:", cols)
    #print("Total Cells:", totalCells)

    i = 0
    j = 0
    xctr = 0
    yctr = 0
    indexer = 0
    while i < rows:
        while j < cols:
            if i == rows - 1:
                cl = Cell(size, xctr, yctr, indexer, "bottomEdge")
                if j == cols - 1:
                    cl = Cell(size, xctr, yctr, indexer, "bottomRightCorner")
                    rightCells.append(cl)
                if j == (cols - 1) - (rows+3):
                    cl = Cell(size, xctr, yctr, indexer, "bottomLeftCorner")
                    leftCells.append(cl)
                bottomCells.append(cl)
                allCells.append(cl)
            elif i == 0:
                cl = Cell(size, xctr, yctr, indexer, "topEdge")
                if j == 0:
                    cl = Cell(size, xctr, yctr, indexer, "topLeftCorner")
                    leftCells.append(cl)
                if j == cols - 1:
                    cl = Cell(size, xctr, yctr, indexer, "topRightCorner")
                    rightCells.append(cl)
                topCells.append(cl)
                allCells.append(cl)

            elif j == 0:
                cl = Cell(size, xctr, yctr, indexer, "leftEdge")
                leftCells.append(cl)
                allCells.append(cl)

            elif j == cols - 1:
                cl = Cell(size, xctr, yctr, indexer, "rightEdge")
                rightCells.append(cl)
                allCells.append(cl)

            else:
                cl = Cell(size, xctr, yctr, indexer, "Regular")
                regularCells.append(cl)
                allCells.append(cl)

            xctr += size
            indexer += 1
            j += 1
        j = 0
        xctr = 0
        yctr += size
        i += 1


def main():
    global regularCells, topCells, bottomCells,\
        rightCells, leftCells, allCells, aliveCells
    pygame.display.init()

    winx = 800
    winy = 600
    screen = pygame.display.set_mode((winx, winy))
    pygame.display.set_caption("Conway's Game of Life")
    done = False

    size = 10
    createCells(winx, winy, size)

    rows = int(winy / size)  # screen width / cell size
    cols = int(winx / size)

    print("Rows:", rows)
    print("Cols:", cols)

    timestep = float(sys.argv[1])
    print("Wait Time:", timestep)

    while not done:
        mPos = pygame.mouse.get_pos()
        decides = 0
        for dd in allCells:
            r = dd.decide(rows, cols)
            if not r:
                decides += 1

        if decides == len(allCells):
            del allCells[:]
            createCells(winx, winy, size)

        ranPoision = random.randint(0, 20)
        if ranPoision == 5:
            # Poision a random individual
            rindx = random.randint(0, len(aliveCells) - 1)
            if not aliveCells[rindx].poisioned and aliveCells[rindx].alive:
                aliveCells[rindx].poisioned = True

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                done = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if timestep < 1.0:
                        timestep += 0.20
                        print("Wait Time:", timestep)
                if e.key == pygame.K_DOWN:
                    if timestep > 0.20:
                        timestep -= 0.20
                    print("Wait Time:", timestep)
                if e.key == pygame.K_ESCAPE:
                    done = True
                if e.key == pygame.K_SPACE:
                    # Poision a random individual
                    rindx = random.randint(0, len(aliveCells)-1)
                    if not aliveCells[rindx].poisioned and aliveCells[rindx].alive:
                        aliveCells[rindx].poisioned = True

        screen.fill((0, 0, 0))

        for cell in allCells:
            cell.draw(screen, mPos)

        pygame.display.flip()
        time.sleep(timestep)


    pygame.display.quit()

main()
