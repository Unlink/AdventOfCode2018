import re
from PIL import Image, ImageDraw

regex = r"position=\< ?([\d-]+), [ ]?([\d-]+)\> velocity=\< ?([\d-]+), [ ]?([\d-]+)\>"

class Point:
    def __init__(self, x, y, wx, wy):
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy
    def move(self):
        self.x += self.wx
        self.y += self.wy
    def moveBack(self):
        self.x -= self.wx
        self.y -= self.wy
    
def calculateRange(points):
    minX = min(points, key=lambda x: x.x).x
    minY = min(points, key=lambda x: x.y).y

    maxX = max(points, key=lambda x: x.x).x
    maxY = max(points, key=lambda x: x.y).y
    
    return (minX, minY, maxX, maxY)
    
def printAsImage(points, name):
    minX, minY, maxX, maxY = calculateRange(points)
    
    img = Image.new('L', (maxX+1-minX, maxY+1-minY))
    for p in points:
        px = p.x - minX
        py = p.y - minY
        img.putpixel((px, py), 255)
        #draw = ImageDraw.Draw(img)
        #draw.ellipse((px-2, py-2, px+2, py+2), fill = 'white', outline ='white')
    img.save(name+'.png')

points = list()

with open("input.txt", "r") as lines:
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            points.append(Point(int(matches.group(1)), int(matches.group(2)), int(matches.group(3)), int(matches.group(4))))
        
minX, minY, maxX, maxY = calculateRange(points)

print("minX "+str(minX))
print("maxX "+str(maxX))
print("minY "+str(minY))
print("maxY "+str(maxY))

lastWidth = maxX - minX

for i in range(1000000):
    for p in points:
        p.move()
    minX, minY, maxX, maxY = calculateRange(points)
    if lastWidth < (maxX - minX):
        printAsImage(points, "result-"+str(i))
        for p in points:
            p.moveBack()
        printAsImage(points, "result2-"+str(i))
        break
        
    lastWidth = maxX - minX

