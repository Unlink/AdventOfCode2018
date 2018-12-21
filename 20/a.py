def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
    
class Cell:
    def __init__(self, x, y, map):
        self.map = map
        self.x = x
        self.y = y
        #up, left, down, right
        self.doors = [False, False, False, False]
        self.distance = 9999
        
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

branches = list()           
for c in path:
    if c == '|':
        room = branches[-1]
    elif c == '(':
        branches.append(room)
    elif c == ')':
        branches.pop()
    else:
        room = room.goTo(dToI[c])
         
mapa.getCell(0,0).distance = 0
toProcess = [mapa.getCell(0,0)]

maxDistance = 0
maxDistanceCell = None

while len(toProcess) > 0:
    room = toProcess.pop(0)
    for i in range(4):
        if room.doors[i] and room.getNeighbour(i).distance > room.distance + 1:
            room.getNeighbour(i).distance = room.distance + 1
            toProcess.append(room.getNeighbour(i))
            if maxDistance < room.getNeighbour(i).distance:
                maxDistance = room.getNeighbour(i).distance
                maxDistanceCell = room.getNeighbour(i)



print((room.x, room.y, room.doors))

minX = min([i[0] for i in mapa.cells.keys()])
maxX = max([i[0] for i in mapa.cells.keys()])
minY = min([i[1] for i in mapa.cells.keys()])
maxY = max([i[1] for i in mapa.cells.keys()])

print((minX, maxX, minY, maxY))
print("Max distance: "+str(maxDistance))

counter = 0
for i in range(minY, maxY+1):
    for j in range(minX, maxX+1):
        if mapa.getCell(j,i).distance >= 1000:
            counter += 1
print("Max distance longer than 1000: "+str(counter))           

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