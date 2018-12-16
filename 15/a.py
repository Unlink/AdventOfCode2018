class EndOfGameException(Exception):
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
    def __init__(self, type):
        self.hitPoints = 200
        self.type = type
        self.position = None
    def moveTo(self, cell):
        if self.position != None:
           self.unit = None
        cell.addUnit(self)
        self.position = cell
    def step(self):
        enemies = findEnemies(self.type)
        if len(enemies) == 0:
            raise EndOfGameException()
        enemiesInRange = self.findEnemiesInRange(enemies)
        if len(enemiesInRange) > 0:
            #attack...
            pass
        else:
            freePositions = self.identifyFreeSquares(enemies)
            if len(freePositions) == 0:
                return
            #print([str(x) for x in freePositions])
     
    def findEnemiesInRange(self, listOfEnemies):
        return [e for e in listOfEnemies if e.position.isInRange(self.position)]
    def identifyFreeSquares(self, listOfEnemies):
        freeSquares = list()
        for enemy in listOfEnemies:
            freeSquares.extend(enemy.position.getFreePositionNearbay())
        return freeSquares
    def calcOrder(self):
        return self.position.calcOrder()
    def __str__(self):
        return "u_"+self.type+"["+str(self.position.x)+","+str(self.position.y)+"]"

cave = list()
units = list()

def findEnemies(type):
    return [u for u in units if u.type != type]

with open("input.txt", "r") as file:
    for line in file:
        row = list()
        for p in line:
            if p == "\n":
                pass
            else:
                cell = Cell(len(row), len(cave), p == "#")
                row.append(cell)
                if not(p == "#" or p == "."):
                    unit = Unit(p)
                    units.append(unit)
                    unit.moveTo(cell)
        cave.append(row)
        
for row in cave:
    for cell in row:
        print(cell, end="")
    print()

units[0].step()    

#while True:
#    units.sort(key=lambda u:u.calcOrder())
#    for unit in units:
#        if unit.hitPoints > 0:
#            unit.step()