import re
regex = r"(\w)=(\d+), \w=(\d+)\.\.(\d+)"

clay = list()
with open("input.txt", "r") as file:
    for line in file:
        matches = re.search(regex, line)
        if matches:
            if matches.group(1) == "x":
                for i in range(int(matches.group(3)), int(matches.group(4))+1):
                    clay.append((int(matches.group(2)), i))
            elif matches.group(1) == "y":
                for i in range(int(matches.group(3)), int(matches.group(4))+1):
                    clay.append((i, int(matches.group(2))))
                    
                    
minX = min(clay, key=lambda e: e[0])[0]-1
maxX = max(clay, key=lambda e: e[0])[0]+1
maxY = max(clay, key=lambda e: e[1])[1]

matrix = [["." for i in range(minX, maxX+2)] for j in range(maxY+1)]

matrix[0][500-minX+1] = "+"

for c in clay:
    matrix[c[1]][c[0]-minX+1] = "#"
    
    
for row in matrix:
    for c in row:
        print(c, end="")
    print()
    
toProcess = list()
toProcess.append((500-minX+1, 0))
while len(toProcess) > 0:
    #toProcess.sort(key = lambda e: e[2])
    cell = toProcess.pop()
#    print("Processing: "+str(cell))
    if cell[1] == maxY:
        continue;
    
    if cell[1]+1 <= maxY and matrix[cell[1]+1][cell[0]] == ".": #can go down
        toProcess.append(cell)
        i = 1
        while cell[1]+i <= maxY and matrix[cell[1]+i][cell[0]] == ".":
            matrix[cell[1]+i][cell[0]] = "|"
            toProcess.append((cell[0], cell[1]+i))
            i += 1
            
        
        if cell[1]+i > maxY:
#            print("hit")
            cell = toProcess.pop()
            cell = toProcess.pop()
#            print(cell)
            while cell[1]+1 <= maxY and matrix[cell[1]+1][cell[0]] != "." and len(toProcess) > 0:
                cell = toProcess.pop()
#                print(cell)
            if len(toProcess) > 0:
                toProcess.append(cell)
        elif matrix[cell[1]+i][cell[0]] == "|":
            ##am i blocked from both sides?
            block1 = False
            block2 = False
            for s in range(0, cell[0]):
                if matrix[cell[1]+i-1][s] != ".":
                    block1 = True

            for s in range(cell[0]+1, len(matrix[0])):
                if matrix[cell[1]+i-1][s] != ".":
                    block2 = True
            if not(block1 and block2):
                cell = toProcess.pop()
                cell = toProcess.pop()
                while len(toProcess) > 0:
                    cell = toProcess.pop()
                if len(toProcess) > 0:
                    toProcess.append(cell)
            
        
    else:
        ##go left
        i = 1
        while matrix[cell[1]][cell[0]-i] == ".":
            matrix[cell[1]][cell[0]-i] = "|"
            toProcess.append((cell[0]-i, cell[1]))
            if matrix[cell[1]+1][cell[0]-i] == ".":
                break
            i += 1
        ##right
        i = 1
        while matrix[cell[1]][cell[0]+i] == ".":
            matrix[cell[1]][cell[0]+i] = "|"
            toProcess.append((cell[0]+i, cell[1]))
            if matrix[cell[1]+1][cell[0]+i] == ".":
                break
            i += 1
    
    
#    print()
#    print()    
#    for row in matrix:
#        for c in row:
#            print(c, end="")
#        print()
water = 0
for row in matrix:
    for c in row:
        if c == "|":
            water += 1
            
print(water)

print()
print()    
for row in matrix:
    for c in row:
        print(c, end="")
    print()