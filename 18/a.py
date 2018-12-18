from PIL import Image, ImageDraw
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def iterateArea(area, x, y):
    surounding = list()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if y+i >= 0 and y+i < len(area) and x+j >= 0 and x+j < len(area[0]) and not(i == j and i == 0):
                surounding.append(area[y+i][x+j])
    return surounding
    
def countE(elements, w):
    return sum([1 for x in elements if x == w])
    
area = list()
print("Initial")
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
