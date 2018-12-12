initialState = list()
rules = [False for i in range(32)]

with open("input.txt", "r") as file:
    initialState = [x == "#" for x in file.readline().replace("initial state:", "").strip()]
    file.readline()
    for line in file:
        index = sum([(2**c) * (1 if line[c] == "#" else 0) for c in range(5)])
        rules[index] = line[9] == "#"
    
#print(initialState)
#print(rules)

state = initialState
zeroIndex = 0
lastIndex = 0

for g in range(10000):
    newState = [False, False] + state + [False, False]
    zeroIndex += 2
    oldState = [False, False, False, False] + state + [False, False, False, False]
    for i in range(len(newState)):
        newState[i] = rules[sum([(2**c) * (1 if oldState[i+c] else 0) for c in range(5)])]
    while not(newState[0]):
        newState.pop(0)
        zeroIndex -= 1
    while not(newState[len(newState)-1]):
        newState.pop()
    print(str(g+1)+"["+str(zeroIndex)+"]"+"".join(["#" if x else "." for x in newState]))
    if state == newState:
        print("wohoho")
        result = 0
        for i in range(len(newState)):
            if newState[i]:
                result += i - zeroIndex - (50000000000 -  g - 1)*(zeroIndex-lastIndex)
        print(result)
        exit()
    state = newState
    lastIndex = zeroIndex
       
print(zeroIndex)       
print(state)

result = 0
for i in range(len(state)):
    if state[i]:
        result += i - zeroIndex
        
print(result) #399999999957
    