class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.area = -1
    def calculateArea(self, matrix):
        self.area = 0
        for i in matrix:
            for j in i:
                if len(j.toPoints) == 1 and self in j.toPoints:
                    self.area += 1
                    
    def __str__(self):
        return str(self.x)+","+str(self.y)+" => "+str(self.area)
        
class PointInSpace:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.minDistance = 10000
        self.toPoints = list()
        
    def applyPoint(self, point):
        distance = self.calculateDistanceTo(point)
        if distance < self.minDistance:
            self.toPoints = [point]
            self.minDistance = distance
        elif distance == self.minDistance:
            self.toPoints.append(point)
    def calculateDistanceTo(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y)
        
points = list()

with open("input.txt", "r") as lines:
    for line in lines:
        parts = line.split(",")
        points.append(Point(int(parts[0].strip()), int(parts[1].strip())))
        
minX = min(points,key=lambda p: p.x).x
maxX = max(points,key=lambda p: p.x).x

minY = min(points,key=lambda p: p.y).y
maxY = max(points,key=lambda p: p.y).y

print(minX)
print(maxX)
print(minY)
print(maxY)

matrix = [[PointInSpace(x+minX,y+minY) for y in range(maxY-minY)] for x in range(maxX-minX)]

locationSize = 0
for i in matrix:
    for j in i:
        distances = 0
        for point in points:
            distances += j.calculateDistanceTo(point)
        if distances < 10000:
            locationSize += 1
            
            
print(locationSize)