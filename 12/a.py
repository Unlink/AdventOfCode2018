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

for g in range(20):
    newState = [False, False] + state + [False, False]
    zeroIndex += 2
    oldState = [False, False, False, False] + state + [False, False, False, False]
    for i in range(len(newState)):
        newState[i] = rules[sum([(2**c) * (1 if oldState[i+c] else 0) for c in range(5)])]
    state = newState
    while not(state[0]):
        state.pop(0)
        zeroIndex -= 1
    while not(state[len(state)-1]):
        state.pop()
    print(str(g+1)+"["+str(zeroIndex)+"]"+"".join(["#" if x else "." for x in state]))
       
print(zeroIndex)       
print(state)

result = 0
for i in range(len(state)):
    if state[i]:
        result += i - zeroIndex
        
print(result)
    