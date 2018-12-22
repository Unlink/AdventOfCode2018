from PIL import Image, ImageDraw

# depth = 6084
# target = (14,709)

# depth = 510
# target = (10,10)

# depth = 4848
# target = (15, 700)

depth = 9171 
target = (7,721)

# depth = 11820 
# target = (7,782)

buffer = 50

def getErrosion(index):
    return (index + depth) % 20183
    
def getType(errosion):
    return [".", "=", "|"][errosion % 3]
    
def getRisk(errosion):
    return errosion % 3
    
allowedTools = {
    '.': ["T", "C"],
    '=': ["", "C"],
    '|': ["", "T"]
}


class Location:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.tools = {}
        self.isFinal = False
    def getAdjecment(self, map):
        adjecment = list()
        if self.x > 0:
            adjecment.append(map[self.y][self.x-1])
        if self.y > 0:
            adjecment.append(map[self.y-1][self.x])
        if self.x+1 < len(map[0]):
            adjecment.append(map[self.y][self.x+1])
        if self.y+1 < len(map):
            adjecment.append(map[self.y+1][self.x])
        return adjecment
        
    def tryToMoveToNext(self, other):
        moved = False
        for tool in allowedTools[self.type]:
            currentDistance = self.getDistanceWithTool(tool)
            #print("Try to move from "+str((self.x, self.y))+"("+self.type+") to "+str((other.x, other.y))+"("+other.type+")  with tool "+tool)
            #print("Distance "+str(currentDistance)+", allowed? "+str(other.isAccessAllowed(tool)))
            if other.isAccessAllowed(tool) and other.getDistanceWithTool(tool) > currentDistance + 1:
                #print("Other distance with tool "+str(other.getDistanceWithTool(tool)))
                other.setDistanceWithTool(tool, currentDistance + 1)
                moved = True
            #elif not(other.isAccessAllowed(tool)) and other.getDistanceWithTool(tool) > currentDistance + 8:
            #    other.setDistanceWithTool(tool, currentDistance + 8)
            #    moved = True
        return moved
    
    def getDistanceWithTool(self, tool):
        if tool in self.tools:
            return self.tools[tool]
        min = 999999999
        for key, value in self.tools.items():
            if min > value:
                min = value
        return min + 7
        
    def setDistanceWithTool(self, tool, distance):
        if self.type == "." and tool == "":
            raise Exception("Cannot be reached")
        if self.type == "=" and tool == "T":
            raise Exception("Cannot be reached")
        if self.type == "|" and tool == "C":
            raise Exception("Cannot be reached")
            
        self.tools[tool] = distance
        
    def calculateMoveCost(self, tool, other):
        return 1 if other.isAccessAllowed(tool) else 7
        
    def isAccessAllowed(self, tool):
        if self.type == ".":
            return tool != ""
        elif self.type == "=":
            return tool != "T"
        elif self.type == "|":
            return tool != "C"

cave = [[0 for i in range(target[0]+buffer)] for j in range(target[1]+buffer)]

for j in range(target[1]+buffer):
    for i in range(target[0]+buffer):
        if i == 0 and j == 0:
            cave[j][i] = 0
        elif (i, j) == target:
            cave[j][i] = 0
        elif i != 0 and j != 0:
            cave[j][i] = getErrosion(cave[j-1][i]) * getErrosion(cave[j][i-1])
        elif i == 0:
            cave[j][i] = j*48271
        elif j == 0:
            cave[j][i] = i*16807
            
for j in range(target[1]+buffer):
    for i in range(target[0]+buffer):
        if i == 0 and j == 0:
            print("M", end="")
        elif (i, j) == target:
            print("T", end="")
        else:
            print(getType(getErrosion(cave[j][i])), end="")
    print()
    
riskLevel = 0
for j in range(target[1]+1):
    for i in range(target[0]+1):
        riskLevel += getRisk(getErrosion(cave[j][i]))
        
print(riskLevel)


cave2 = [[Location(x, y, getType(getErrosion(cave[y][x]))) for x in range(target[0]+buffer)] for y in range(target[1]+buffer)]

cave2[0][0].tools['T'] = 0

toProcess = list([cave2[0][0]])

while len(toProcess):
    current = toProcess.pop(0)
    #print("Processing "+str((current.x, current.y)))
    for next in current.getAdjecment(cave2):
        if current.tryToMoveToNext(next):
            toProcess.append(next)
            
            
print("Calculated nearest path")
print(cave2[target[1]][target[0]].tools)

# for j in range(target[1]+buffer):
    # for i in range(target[0]+buffer):
        # print(getType(getErrosion(cave[j][i]))+str(cave2[j][i].tools), end=";")
    # print()

#print path?
# currentNode = cave2[target[1]][target[0]]
# while currentNode.x != 0 or currentNode.y != 0:
    # print(str((currentNode.x, currentNode.y))+str(currentNode.tools))

    # min = 9999999
    # for next in currentNode.getAdjecment(cave2):
        # for tool, distance in next.tools.items():
            # if distance < min:
                # currentNode = next
                # min = distance
# print(str((currentNode.x, currentNode.y))+str(currentNode.tools))

# img = Image.new('RGB', (len(cave2[0])*5, len(cave2)*5))
# y = 0
# for row in cave2:
    # x = 0
    # for c in row:
        # color = (0, 0, 0)
        # if c.type == ".":
            # color = (100, 100, 100)
        # if c.type == "|":
            # color = (255, 255, 0)
        # if c.type == "=":
            # color = (0, 0, 200)
        
        # for aa in range(4):
            # for bb in range(4):
                # img.putpixel((x*5+aa, y*5+bb), color)
        # x += 1
    # y += 1
# draw = ImageDraw.Draw(img) 
# draw.line((100,200, 150,300), fill=128)
# img.save('result.png')