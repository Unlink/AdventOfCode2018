class EndOfGameException(Exception):
    pass
    
class DeadElf(Exception):
    pass

class Cell: 
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.wall = wall
        self.unit = None
        
    def addUnit(self, unit):
        if not(self.isFree()):
            raise Exception("Cannot move unit to "+str(self.x)+","+str(self.y))
        self.unit = unit
        
    def isFree(self):
        return not(self.wall) and self.unit == None
    def isInRange(self, other):
        if self.x == other.x and (self.y == other.y + 1 or self.y == other.y - 1):
            return True
        elif self.y == other.y and (self.x == other.x + 1 or self.x == other.x - 1):
            return True
        return False
    def getFreePositionNearbay(self):
        positions = list()
        if cave[self.y+1][self.x].isFree():
            positions.append(cave[self.y+1][self.x])
        if cave[self.y-1][self.x].isFree():
            positions.append(cave[self.y-1][self.x])
        if cave[self.y][self.x+1].isFree():
            positions.append(cave[self.y][self.x+1])
        if cave[self.y][self.x-1].isFree():
            positions.append(cave[self.y][self.x-1])
        
        return positions
    def calcOrder(self):
        return self.y * 1000 + self.x #can change 1000 to width of maze
    def __str__(self):
        if self.wall:
            return "#"
        elif self.unit == None:
            return "."
        else:
            return self.unit.type
        
class Unit:
    def __init__(self, type, power):
        self.hitPoints = 200
        self.attack = power
        self.type = type
        self.position = None
    def moveTo(self, cell):
        if self.position != None:
           self.position.unit = None
        cell.addUnit(self)
        self.position = cell
    def step(self):
        enemies = findEnemies(self.type)
        if len(enemies) == 0:
            raise EndOfGameException()
        enemiesInRange = self.findEnemiesInRange(enemies)
        if Debug:
            print("Enemies in range of "+str(self) + ":" + ";".join([str(e) for e in enemiesInRange]))
        if len(enemiesInRange) == 0:
            freePositions = self.identifyFreeSquares(enemies)
            if len(freePositions) == 0:
                return
            positionDistances = [(p, self.calculateDistance(p)) for p in freePositions]
            positionDistances.sort(key = lambda x: (x[1][self.position.y][self.position.x], x[0].calcOrder()))
            if Debug:
                print("Distance to free positions for "+str(self) + ":" + ";".join([str(e[0].x)+","+str(e[0].y)+"d:"+str(e[1][self.position.y][self.position.x]) for e in positionDistances]))
            #print(positionDistances)
            #print(str(positionDistances[0][0].x) + "," + str(positionDistances[0][0].y))
            cellToMove = self.calculateMove(positionDistances[0][1])
            if cellToMove == NoneCell: #non free path
                return
            if Debug:
                print("Calculated move for "+str(self) + ":" + str(cellToMove.x)+","+str(cellToMove.y))
            self.moveTo(cellToMove)
            enemiesInRange = self.findEnemiesInRange(enemies)
            
        #enemies = findEnemies(self.type)
        #if len(enemies) == 0:
        #    raise EndOfGameException()
        enemiesInRange.sort(key = lambda x: (x.hitPoints, x.calcOrder()))
        if len(enemiesInRange) > 0:
            enemy = enemiesInRange[0]
            enemy.hit(self.attack)
        
            
    def findEnemiesInRange(self, listOfEnemies):
        return [e for e in listOfEnemies if e.position.isInRange(self.position)]
    def identifyFreeSquares(self, listOfEnemies):
        freeSquares = list()
        for enemy in listOfEnemies:
            freeSquares.extend(enemy.position.getFreePositionNearbay())
        return freeSquares
    def calculateDistance(self, position):
        distMatrix = [[9999 if cell.isFree() else None for cell in row] for row in cave]
        distMatrix[self.position.y][self.position.x] = 9999 #current cell is acesible
        front = list()
        distMatrix[position.y][position.x] = 0
        front.append((position.y, position.x))
        
        while len(front) > 0:
            element = front.pop(0)
            distance = distMatrix[element[0]][element[1]] + 1
            
            if distMatrix[element[0]+1][element[1]] != None and distMatrix[element[0]+1][element[1]] > distance:
                distMatrix[element[0]+1][element[1]] = distance
                front.append((element[0]+1, element[1]))
            
            if distMatrix[element[0]-1][element[1]] != None and distMatrix[element[0]-1][element[1]] > distance:
                distMatrix[element[0]-1][element[1]] = distance
                front.append((element[0]-1, element[1]))
                
            if distMatrix[element[0]][element[1]+1] != None and distMatrix[element[0]][element[1]+1] > distance:
                distMatrix[element[0]][element[1]+1] = distance
                front.append((element[0], element[1]+1))
                
            if distMatrix[element[0]][element[1]-1] != None and distMatrix[element[0]][element[1]-1] > distance:
                distMatrix[element[0]][element[1]-1] = distance
                front.append((element[0], element[1]-1))
        
        #for row in distMatrix:
        #    for cell in row:
        #        print("None" if cell == None else str(cell).zfill(4), end="")
        #    print()
        #print()
        return distMatrix 
    def calculateMove(self, matrix):
        min = 9999-1
        minCellToMove = NoneCell
        
        if matrix[self.position.y+1][self.position.x] != None and matrix[self.position.y+1][self.position.x] < min or (matrix[self.position.y+1][self.position.x] == min and cave[self.position.y+1][self.position.x].calcOrder() < minCellToMove.calcOrder()):
            min = matrix[self.position.y+1][self.position.x]
            minCellToMove = cave[self.position.y+1][self.position.x]
        
        if matrix[self.position.y-1][self.position.x] != None and matrix[self.position.y-1][self.position.x] < min or (matrix[self.position.y-1][self.position.x] == min and cave[self.position.y-1][self.position.x].calcOrder() < minCellToMove.calcOrder()):
            min = matrix[self.position.y-1][self.position.x]
            minCellToMove = cave[self.position.y-1][self.position.x]
            
        if matrix[self.position.y][self.position.x+1] != None and matrix[self.position.y][self.position.x+1] < min or (matrix[self.position.y][self.position.x+1] == min and cave[self.position.y][self.position.x+1].calcOrder() < minCellToMove.calcOrder()):
            min = matrix[self.position.y][self.position.x+1]
            minCellToMove = cave[self.position.y][self.position.x+1]
            
        if matrix[self.position.y][self.position.x-1] != None and matrix[self.position.y][self.position.x-1] < min or (matrix[self.position.y][self.position.x-1] == min and cave[self.position.y][self.position.x-1].calcOrder() < minCellToMove.calcOrder()):
            min = matrix[self.position.y][self.position.x-1]
            minCellToMove = cave[self.position.y][self.position.x-1]
            
        return minCellToMove
    def hit(self, power):
        self.hitPoints -= power
        if self.hitPoints <= 0:
            units.remove(self)
            self.position.unit = None
            if self.type == "E":
                raise DeadElf()
    def calcOrder(self):
        return self.position.calcOrder()
    def __str__(self):
        return "u_"+self.type+"["+str(self.position.x)+","+str(self.position.y)+"]"

def findEnemies(type):
    return [u for u in units if u.type != type]

for power in range(4, 100):
    cave = list()
    units = list()
    NoneCell = Cell(9999,9999, True)
    Debug = False


    with open("input.txt", "r") as file:
        for line in file:
            row = list()
            for p in line:
                if p == "\n":
                    pass
                elif p == " ":
                    break
                else:
                    cell = Cell(len(row), len(cave), p == "#")
                    row.append(cell)
                    if not(p == "#" or p == "."):
                        unit = Unit(p, power if p == "E" else 3)
                        units.append(unit)
                        unit.moveTo(cell)
            cave.append(row)
            
    for row in cave:
        for cell in row:
            print(cell, end="")
        print()

    fullRoundCompleted = 0
    try:
        while True:
            units.sort(key=lambda u:u.calcOrder())
            tempUnits = list([u for u in units])
            for unit in tempUnits:  
                if unit.hitPoints > 0:
                    unit.step()
            print("After "+str(fullRoundCompleted+1)+" round")
            for row in cave:
                for cell in row:
                    print(cell, end="")
                for cell in row:
                    if cell.unit != None:
                        print("\t"+str(cell.unit.type)+"("+str(cell.unit.hitPoints)+")", end="")
                print()
            fullRoundCompleted += 1
            #if fullRoundCompleted == 1:
            #    Debug = True
    except EndOfGameException:
        print("Last state")
        for row in cave:
            for cell in row:
                print(cell, end="")
            print()
        
        sumOfHitpoints = sum([u.hitPoints for u in units])
        print("Sum of hitpoints: "+str(sumOfHitpoints))
        print(fullRoundCompleted * sumOfHitpoints) 
        raise
    except DeadElf:
        print(str(power)+" is not enough")
        