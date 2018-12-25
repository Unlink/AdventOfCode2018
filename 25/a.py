class Point:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.constelation = -1
        
    def distance(self, other):
        return abs(self.a - other.a) + abs(self.b - other.b) + abs(self.c - other.c) + abs(self.d - other.d)
       
    def __str__(self):
        return str((self.a, self.b, self.c, self.d))+str(self.constelation)
    
points = list() 

with open("input.txt", "r") as lines:
    constelation = 1
    for line in lines:
        coords = [int(x) for x in line.strip().split(",")]
        point = Point(coords[0], coords[1], coords[2], coords[3])
        point.constelation = constelation
        constelation += 1
        for p in points:
            if p.distance(point) <= 3:
                for x in [x for x in points if x.constelation == p.constelation]:
                    x.constelation = point.constelation
        points.append(point)
        
print("Constelations: "+str(len(set([x.constelation for x in points]))))

for p in points:
    print(p)