import re
from math import sqrt

regex = r"(\d+) units each with (\d+) hit points (\((\w+) to ([\w, ]+)(; (\w+) to ([\w, ]+))?\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)"

class Group:
    def __init__(self, id, team, record, boost):
        self.id = id
        self.team = team
        matches = re.search(regex, record)
        if matches:
            self.units = int(matches.group(1))
            self.hitPoints = int(matches.group(2))
            self.weak = list()
            self.immune = list()
            if matches.group(4) == "weak":
                self.weak = matches.group(5).split(", ")
            if matches.group(4) == "immune":
                self.immune = matches.group(5).split(", ")
            if matches.group(7) == "weak":
                self.weak = matches.group(8).split(", ")
            if matches.group(7) == "immune":
                self.immune = matches.group(8).split(", ")
            self.damage = int(matches.group(9)) + boost
            self.attackType = matches.group(10)
            self.initiative = int(matches.group(11))
        else:
            raise Exception("Cannot parse "+str(record))
        
    def __str__(self):
        return str(self.id)+"["+self.team+"]" + str(self.units) + "("+str([self.hitPoints, self.damage, self.attackType, self.initiative])+")"+"weak"+str(self.weak)+" immune"+str(self.immune)
        
    def getAttackStrength(self, otherUnit):
        if self.attackType in otherUnit.immune:
            return 0
        elif self.attackType in otherUnit.weak:
            return 2 * self.getEffectivePower()
        else:
            return self.getEffectivePower()
    
    def getEffectivePower(self):
        return self.damage * self.units
        
    def attack(self):
        unitsToKill = int(self.getAttackStrength(self.attacking) / self.attacking.hitPoints)
        # print(self.team + " group " + str(self.id) + " attacks " + self.attacking.team + " group " + str(self.attacking.id) + " killing " + str(unitsToKill))
            
        self.attacking.units -= unitsToKill
        return unitsToKill
        

def combat(boost):
    groups = list()     
    with open("input.txt", "r") as lines:
        team = ""
        id = 1
        for line in lines:
            if line.strip().endswith(":"):
                team = line.strip()
                id = 1
            elif line.strip() != "":
                groups.append(Group(id, team, line, boost if team == "Immune System:" else 0))
                id += 1
                
    # for g in groups:
        # print(str(g))
               
    round = 1
    while len(set([g.team for g in groups])) == 2:
        # print("Round "+str(round))
        groups.sort(key=lambda g:(g.team), reverse=True)
        #for g in groups:
        #    print(str(g))
        round += 1
        for g in groups:
            g.attacking = None
            g.attackedBy = None
            
        #print("Selectiong phase")
        groups.sort(key=lambda g:(g.getEffectivePower(), g.initiative), reverse=True)
        for g in groups:
            toAttack = [(x, g.getAttackStrength(x)) for x in groups if x.team != g.team and x.attackedBy == None and g.getAttackStrength(x) > 0]
            toAttack.sort(key=lambda x: (x[1], x[0].getEffectivePower(), x[0].initiative), reverse=True)
            # for x in toAttack:
                # print(g.team + " group " + str(g.id) + " would deal defending " + x[0].team + " group " + str(x[0].id) + " damage " + str(g.getAttackStrength(x[0])))
                
            if len(toAttack) > 0:
                g.attacking = toAttack[0][0]
                g.attacking.attackedBy = g
        #print("Attak phase")    
        groups.sort(key=lambda g:g.initiative, reverse=True)
        killed = 0
        for g in groups:
            if g.units > 0 and g.attacking != None:
                killed += g.attack()
        if killed == 0:
            return ("draw", sum([g.units for g in groups]))
        toRemove = [g for g in groups if g.units <= 0]
        for g in toRemove:
            groups.remove(g)
        #print()
    return (groups[0].team, sum([g.units for g in groups]))

result = combat(0)
print("Winning team: "+result[0]+" score: "+str(result[1]))
for i in range(1000):
    print("Boost "+str(i))
    result = combat(i)
    print("Winning team: "+result[0]+" score: "+str(result[1]))
    if result[0] == "Immune System:":
        break