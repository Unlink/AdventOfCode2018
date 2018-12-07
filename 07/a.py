import re
from string import ascii_uppercase

regex = r"Step ([A-Z]) must be finished before step ([A-Z]) can begin."

class Step:
    
    def __init__(self, c):
        self.c = c
        self.depends = list()
        self.done = False
    def addDependant(self, step):
        self.depends.append(step)
        
    def isAvailable(self):
        for d in self.depends:
            if not(d.done):
                return False
        return True

steps = dict()
for c in ascii_uppercase:
    steps[c] = Step(c)
        
with open("input.txt", "r") as lines:
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            steps[matches.group(2)].addDependant(steps[matches.group(1)])
            
            
while True:
    available = list()
    for i, step in steps.items():
        if not(step.done) and step.isAvailable():
            available.append(step)
    
    if len(available) == 0:
        break
    selected = min(available, key=lambda x: x.c)
    selected.done = True
    print(selected.c, end="")
    