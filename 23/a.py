import re
from math import sqrt

regex = r"pos=<([0-9-]+),([0-9-]+),([0-9-]+)>, r=([0-9-]+)"

class PointInSpace:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def distanceTo(self, other):
        return abs(self.x - other.x)+abs(self.y - other.y)+abs(self.z - other.z)

class Bot(PointInSpace):
    
    def __init__(self, x,y,z,range):
        super().__init__(x,y,z)
        self.range = range
    
    def inRange(self, other):
        return self.distanceTo(other) <= self.range
        
class Area(PointInSpace):
    def __init__(self, x,y,z,size):
        super().__init__(x,y,z)
        self.size = size
    
    def inRange(self, bot):
        return self.distanceTo(bot) <= self.size + bot.range
        

bots = list()
        
with open("input.txt", "r") as lines:
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            bots.append(Bot(int(matches.group(1)), int(matches.group(2)), int(matches.group(3)), int(matches.group(4))))
            
strongest = max(bots, key=lambda x: x.range)

print("In range of strongest bot")
print(len([x for x in bots if strongest.inRange(x)]))

print("coors ranges:")
bounds = {}
for i in ["x","y","z"]:
    bounds[i] = (min([getattr(x, i) for x in bots]), max([getattr(x, i) for x in bots]))
print(bounds)

mx = my = mz = 0

for i in range(9):
    multiplier = 10**(8-i)
    print("Calculating with multiplier "+str(multiplier))
    maxBotsInRange = 0
    bigArea = None
    for x in range(-10, 11):
        for y in range(-10, 11):
            for z in range(-10, 11):
                area = Area(mx + x*multiplier, my + y*multiplier, mz + z*multiplier, multiplier * sqrt(3)-1)
                botsInRange = len([a for a in bots if area.inRange(a)])
                if botsInRange > maxBotsInRange:
                    maxBotsInRange = botsInRange
                    bigArea = area
                elif botsInRange == maxBotsInRange and botsInRange > 0:
                    if area.distanceTo(PointInSpace(0,0,0)) < bigArea.distanceTo(PointInSpace(0,0,0)):
                        bigArea = area
    mx = bigArea.x
    my = bigArea.y
    mz = bigArea.z
    print(mx, my, mz, maxBotsInRange)
    
print(mx + my + mz)