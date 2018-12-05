import re

regex = r"\[([\d-]+) ([\d]+):([\d]+)\] (.*)"
regex2 = r"Guard #(\d+) begins shift"

class Record:
    def __init__(self, line):
        matches = re.search(regex, line)
        if matches:
            self.date = matches.group(1)
            self.hour = int(matches.group(2))
            self.minute = int(matches.group(3))
            self.action = matches.group(4)
        else:
            raise ValueError('Wrong format.')
    def __str__(self):
        return (str(self.date) + " " + str(self.hour) + ":" + str(self.minute) + " - " + str(self.action))
        
class Guard:
    def __init__(self, id):
        self.id = id
        self.works = list()
        self.current = [False for x in range(60)]
        self.fallsAsleep = 0
    def apply(self, record):
        if record.action == "falls asleep":
            self.fallsAsleep = record.minute
        if record.action == "wakes up":
            for i in range(self.fallsAsleep, record.minute):
                self.current[i] = True
        
    def finish(self):
        self.works.append(self.current)
        self.current = [False for x in range(60)]
        
    def printWork(self):
        for day in self.works:
            for minute in day:
                print("X" if minute else ".", end="")
            print()
    def sleepTime(self):
        return len([1 for i, row in enumerate(self.works) for j, value in enumerate(row) if value])
        
    def calculateSleepTimes(self):
        sleepTimes = [0 for x in range(60)]
        for day in self.works:
            for i in range(60):
                if day[i]:
                    sleepTimes[i] += 1
                    
        return sleepTimes.index(max(sleepTimes))
        

records = list()

with open("input.txt", "r") as lines:
    for line in lines:
        records.append(Record(line))
        
records.sort(key=lambda x: x.date + str(x.hour) + str(x.minute), reverse=False)

guards = dict()
guard = None
   
for record in records:
    matches = re.search(regex2, record.action)
    if matches:
        if guard != None:
            guard.finish()
            
        id = int(matches.group(1))
        if id in guards:
            guard = guards[id]
        else:
            guard = Guard(id)
            guards[id] = guard
    else:
        guard.apply(record)

        
print("000000000011111111112222222222333333333344444444445555555555")
print("012345678901234567890123456789012345678901234567890123456789")

for i, guard in guards.items():
    print("#"+str(guard.id) + " Sleap time = "+str(guard.sleepTime()))
    guard.printWork()
    
    
i, maxSleapyGuard = max(guards.items(), key=lambda g: g[1].sleepTime())

print(maxSleapyGuard.id)
print(maxSleapyGuard.calculateSleepTimes())

print(maxSleapyGuard.id * maxSleapyGuard.calculateSleepTimes())