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
    
    
class Map:
    def __init__(self):
        self.beginCell = Cell(0, 0)
        self.cells = dict()
        self.cells[(0,0)] = self.beginCell
        
    
with open("input.txt", "r") as file:
    for line in file:
        area.append(line.strip())
        print(line.strip())
        
timer = 0
while True:
    newArea = [[c for c in row] for row in area]
    
    i = 0
    for row in area:
        j = 0
        for cell in row:
            surounding = iterateArea(area, j, i)
            #print("["+str(i)+":"+str(j)+"] - "+str(surounding))
            if cell == "." and countE(surounding, "|") >= 3:
                newArea[i][j] = "|"
            elif cell == "|" and countE(surounding, "#") >= 3:
                newArea[i][j] = "#"
            elif cell == "#":
                if not(countE(surounding, "#") >= 1 and countE(surounding, "|") >= 1):
                    newArea[i][j] = "."
            j+=1
        i+=1
    area = newArea
    
    timer += 1
    print("After" + str(timer))
    
    for row in area:
        print("".join(row))
    time.sleep(.1)
    #print(chr(27) + "[2J")
    
    if timer == 10:
        break;
        
wood = 0
lumberyards = 0
for row in area:
    wood += countE(row, "|")
    lumberyards += countE(row, "#")
    
print("Wood: "+str(wood))
print("Lumberyards: "+str(lumberyards))
print(str(wood * lumberyards))
