class Track: 
    def __init__(self, x, y, orientation, vagon):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.vagon = vagon
        
    def addVagon(self, vagon):
        if self.vagon != None:
            print("Colision in: "+str(self.x)+":"+str(self.y))
            vagon.removed = True
            self.vagon.removed = True
            self.vagon = None
        else:
            self.vagon = vagon
        
    def __str__(self):
        return self.orientation if self.vagon == None else self.vagon.orientation

class Vagon:
    def __init__(self, x, y, orientation):
        self.orientation = orientation
        self.x = x
        self.y = y
        self.lastMove = 0
        self.removed = False
    def move(self, paths):
        #print("Moving from ["+str(self.x)+", "+str(self.y)+"] to "+self.orientation)
    
        if self.orientation == ">":
            paths[self.y][self.x].vagon = None  
            paths[self.y][self.x+1].addVagon(self)
            
            if paths[self.y][self.x+1].orientation == "-":
                pass
            elif paths[self.y][self.x+1].orientation == "/":
                self.orientation = "^"
            elif paths[self.y][self.x+1].orientation == "\\":
                self.orientation = "v"
            elif paths[self.y][self.x+1].orientation == "+":
                if self.lastMove == 0:
                    self.orientation = "^"
                if self.lastMove == 2:
                    self.orientation = "v"
                self.lastMove = (self.lastMove + 1) % 3
            self.x += 1
        elif self.orientation == "<":
            paths[self.y][self.x].vagon = None
            paths[self.y][self.x-1].addVagon(self)
            if paths[self.y][self.x-1].orientation == "-":
                pass
            elif paths[self.y][self.x-1].orientation == "/":
                self.orientation = "v"
            elif paths[self.y][self.x-1].orientation == "\\":
                self.orientation = "^"
            elif paths[self.y][self.x-1].orientation == "+":
                if self.lastMove == 0:
                    self.orientation = "v"
                if self.lastMove == 2:
                    self.orientation = "^"
                self.lastMove = (self.lastMove + 1) % 3
            self.x -= 1
        elif self.orientation == "v":
            paths[self.y][self.x].vagon = None
            paths[self.y+1][self.x].addVagon(self)
            if paths[self.y+1][self.x].orientation == "|":
                pass
            elif paths[self.y+1][self.x].orientation == "/":
                self.orientation = "<"
            elif paths[self.y+1][self.x].orientation == "\\":
                self.orientation = ">"
            elif paths[self.y+1][self.x].orientation == "+":
                if self.lastMove == 0:
                    self.orientation = ">"
                if self.lastMove == 2:
                    self.orientation = "<"
                self.lastMove = (self.lastMove + 1) % 3
            self.y += 1
        elif self.orientation == "^":
            paths[self.y][self.x].vagon = None
            paths[self.y-1][self.x].addVagon(self)
            if paths[self.y-1][self.x].orientation == "|":
                pass
            elif paths[self.y-1][self.x].orientation == "/":
                self.orientation = ">"
            elif paths[self.y-1][self.x].orientation == "\\":
                self.orientation = "<"
            elif paths[self.y-1][self.x].orientation == "+":
                if self.lastMove == 0:
                    self.orientation = "<"
                if self.lastMove == 2:
                    self.orientation = ">"
                self.lastMove = (self.lastMove + 1) % 3
            self.y -= 1
        
def printPath(path):
    for row in path:
        for cell in row:
            if cell == None:
                print(" ", end="")
            else:
                print(cell, end="")
        print("")

path = list()

with open("input.txt", "r") as file:
    for line in file:
        row = list()
        for p in line:
            if p == "\n":
                pass
            elif p == " ":
                row.append(None)
            else:
                orientation = p
                vagon = None
                if p == "<" or p == ">":
                    orientation = "-"
                    vagon = Vagon(len(row), len(path), p)
                elif p == "v" or p == "^":
                    orientation = "|"
                    vagon = Vagon(len(row), len(path), p)
                row.append(Track(len(row), len(path), orientation, vagon))
        path.append(row)
        
printPath(path)

while(1==1):
    toMove = list()
    for row in path:
        for cell in row:
            if not(cell == None) and not(cell.vagon == None):
                toMove.append(cell.vagon)
    for vagon in toMove:
        if not(vagon.removed):
            vagon.move(path)
    print(len([v for v in toMove if not(v.removed)]))
    if len([v for v in toMove if not(v.removed)]) == 1:
        vagon = [v for v in toMove if not(v.removed)][0]
        print(str(vagon.x)+","+str(vagon.y))
        exit()
    #print()
    #printPath(path)