import re
from string import ascii_uppercase

regex = r"Step ([A-Z]) must be finished before step ([A-Z]) can begin."

class Step:
    
    def __init__(self, c):
        self.c = c
        self.depends = list()
        self.done = False
        self.processing = False
    def addDependant(self, step):
        self.depends.append(step)
        
    def isAvailable(self):
        if self.processing:
            return False
        for d in self.depends:
            if not(d.done):
                return False
        return True
        
    def time(self):
        return ord(self.c)-64
        
class Worker:
    def __init__(self):
        self.endTime = 0
        self.task = None

steps = dict()
for c in ascii_uppercase:
    steps[c] = Step(c)
    
workers = [Worker(), Worker(), Worker(), Worker(), Worker()]
        
with open("input.txt", "r") as lines:
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            steps[matches.group(2)].addDependant(steps[matches.group(1)])
            
           
          
actualTime = 0          
while True:
    freeWorkrers = [worker for worker in workers if worker.task==None]
    if len(freeWorkrers) > 0:
        available = list()
        for i, step in steps.items():
            if not(step.done) and step.isAvailable():
                available.append(step)
        
        if len(available) > 0:
            selected = min(available, key=lambda x: x.c)
            selected.processing = True
            print(selected.c, end="")
            freeWorkrers[0].task = selected;
            freeWorkrers[0].endTime = actualTime + 60 + selected.time()
        else:
            if len([step for i, step in steps.items() if not(step.processing)]) > 0:
                minWorker = min([worker for worker in workers if not(worker.task == None)], key=lambda w: w.endTime)
                minWorker.task.done = True
                actualTime = minWorker.endTime
                minWorker.task = None
            else:
                break;
        
    else:
        minWorker = min(workers, key=lambda w: w.endTime)
        minWorker.task.done = True
        actualTime = minWorker.endTime
        minWorker.task = None
        
lastWorker = max(workers, key=lambda w: w.endTime)

print(lastWorker.endTime)