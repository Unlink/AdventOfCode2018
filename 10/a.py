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
    

points = list()

with open("input.txt", "r") as lines:
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            points.append(Point(int(matches.group(1)), int(matches.group(2)), int(matches.group(3)), int(matches.group(4))))
        
minX = min(points, key=lambda x: x.x).x
minY = min(points, key=lambda x: x.y).y

maxX = max(points, key=lambda x: x.x).x
maxY = max(points, key=lambda x: x.y).y

print("minX "+str(minX))
print("maxX "+str(maxX))
print("minY "+str(minY))
print("maxY "+str(maxY))

print(len(points))

#cca -50 000 to 50 000 => platno pre -100 000 : 100 000 => takze 2000x2000
for i in range(1000000):
    for p in points:
        p.move()
    if i%500 == 0:
        img = Image.new('L', (2000, 2000))
        for p in points:
            #img.putpixel((int(p.x/100) + 1000, int(p.y/100) + 1000), 255)
            px = int(p.x/100) + 1000
            py = int(p.y/100) + 1000
            
            draw = ImageDraw.Draw(img)
            draw.ellipse((px-2, py-2, px+2, py+2), fill = 'white', outline ='white')
        img.save('step'+str(int(i))+'.png')
        print(i)

