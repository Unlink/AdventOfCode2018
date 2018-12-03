import re

regex = r"\#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)"

class Claim:
    def __init__(self, line):
        matches = re.search(regex, line)
        if matches:
            self.id = int(matches.group(1))
            self.x = int(matches.group(2))
            self.y = int(matches.group(3))
            self.w = int(matches.group(4))
            self.h = int(matches.group(5))
        else:
            raise ValueError('Wrong format.')
    def __str__(self):
        return ("Claim: #" + str(self.id) + " @ " + str(self.x) + ", " + str(self.y) + " : "+ str(self.w) + ":" + str(self.h))
    def claim(self, fabric):
        for i in range(self.w):
            for j in range(self.h):
                fabric[self.x + i][self.y + j] += 1;

claims = list()

with open("input.txt", "r") as lines:
    for line in lines:
        claims.append(Claim(line))
        
fabric = [[0 for x in range(1000)] for y in range(1000)] 

for claim in claims:
    claim.claim(fabric)
    
print(len([1 for i, row in enumerate(fabric) for j, value in enumerate(row) if value > 1]))