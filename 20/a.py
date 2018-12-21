def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
    
class Cell:
    def __init__(self, x, y, map):
        self.map = map
        self.x = x
        self.y = y
        #up, left, down, right
        self.doors = [False, False, False, False]
        
    def getPosition(self):
        return (self.x, self.y)
    
    def getNeighbour(self, direction):
        if direction == 0:
            return self.map.getCell(self.x, self.y-1)
        if direction == 1:
            return self.map.getCell(self.x-1, self.y)
        if direction == 2:
            return self.map.getCell(self.x, self.y+1) 
        if direction == 3:
            return self.map.getCell(self.x+1, self.y)
    def goTo(self, direction):
        neighbour = self.getNeighbour(direction)
        self.doors[direction] = True
        neighbour.doors[(direction + 2) % 4] = True
        return neighbour
    
    
class Map:
    def __init__(self):
        self.cells = dict()
        
    def getCell(self, x, y):
        if not((x, y) in self.cells):
            self.cells[(x,y)] = Cell(x,y,self)
        return self.cells[(x,y)]
        
class Branhes:
    def __init__(self, cell, restOfPath, steps):
        self.cell = cell
        self.branches = list()
        self.steps = steps
        #scan for branches
        temp = ""
        phatenties = 0
        for c in restOfPath:
            if c == '|' and phatenties == 0:
                self.branches.append(temp)
                temp = ""
            elif c == '(':
                phatenties += 1
                temp += c
            elif c == ')' and phatenties > 0:
                phatenties -= 1
                temp += c
            elif c == ')' and phatenties == 0:
                self.branches.append(temp)
                temp = ""
            else:
                temp += c
        for i in range(len(self.branches)):
            self.branches[i] += temp
            
    def getBranch(self):
        if self.hasMoreBranches():
            return self.branches.pop()
        else:   
            return None
    def hasMoreBranches(self):
        return len(self.branches) > 0
        
dToI = {
    'N': 0,
    'W': 1,
    'S': 2,
    'E': 3
}
regex = "^$"
with open("input.txt", "r") as file:
    regex = file.read().strip()
        
path = regex[1:-1]

mapa = Map()
room = mapa.getCell(0,0)
branchStack = list()
branchStack.append(Branhes(room, path+")", 0))
steps = 0

while len(branchStack) > 0:
    branch = branchStack.pop()
    if branch.hasMoreBranches():
        branchStack.append(branch)
        path = branch.getBranch()
        room = branch.cell
        for i in range(len(path)):
            if path[i] == "(":
                branchStack.append(Branhes(room, path[i+1:], 0))
                break
            else:
                room = room.goTo(dToI[path[i]])
    
        
        
print((room.x, room.y, room.doors))

minX = min([i[0] for i in mapa.cells.keys()])
maxX = max([i[0] for i in mapa.cells.keys()])
minY = min([i[1] for i in mapa.cells.keys()])
maxY = max([i[1] for i in mapa.cells.keys()])

print((minX, maxX, minY, maxY))

for i in range(minY, maxY+1):
    for j in range(minX, maxX+1):
        cell = mapa.getCell(j,i)
        print("#"+("-" if cell.doors[0] else "#"), end="")
    print("#")
    for j in range(minX, maxX+1):
        cell = mapa.getCell(j,i)
        print(("|" if cell.doors[1] else "#")+("X" if (i,j) == (0,0) else "."), end="")
    print("#")
print("#"*((maxX - minX + 1)*2+1))