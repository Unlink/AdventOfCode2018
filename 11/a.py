input = 9005
fuelGrid = [[(int((((x+1+10)*(y+1)+input)*(x+1+10))/100)%10)-5 for y in range(300)] for x in range(300)]

maxPower = 0
maxCoords = (0, 0, 0)

for z in range(1,300):
    for i in range(300-z):
        for j in range(300-z):        
            power = sum([sum(fuelGrid[x][y] for y in range(j, j+z)) for x in range(i, i+z)])
            if power > maxPower:
                maxPower = power
                maxCoords = (i+1, j+1, z)

print(maxPower)        
print(maxCoords)
