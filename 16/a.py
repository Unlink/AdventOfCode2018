class Instruction:
    def __init__(self, name):
        if not(name in dir(self)):
            raise Exception("Instruction not exists")
        self.name = name
        
    def execute(self, cpu, a, b, c):
        func = getattr(self,self.name)
        func(cpu, a, b, c)
        
    def addr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] + cpu[b]
        
    def addi(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] + b
        
    def mulr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] * cpu[b]
        
    def muli(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] * b
        
    def banr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] & cpu[b]
        
    def bani(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] & b
        
    def borr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] | cpu[b]
        
    def bori(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a] | b
        
    def setr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = cpu[a]
        
    def seti(self, cpu, a, b, c):
        if not(self.checkRegister(c)): return False
        cpu[c] = a
        
    def gtir(self, cpu, a, b, c):
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = 1 if a > cpu[b] else 0
        
    def gtri(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = 1 if cpu[a] > b else 0 
    
    def gtrr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = 1 if cpu[a] > cpu[b] else 0
        
    def eqir(self, cpu, a, b, c):
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = 1 if a == cpu[b] else 0
        
    def eqri(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = 1 if cpu[a] == b else 0 
    
    def eqrr(self, cpu, a, b, c):
        if not(self.checkRegister(a)): return False
        if not(self.checkRegister(b)): return False
        if not(self.checkRegister(c)): return False
        cpu[c] = 1 if cpu[a] == cpu[b] else 0
        
    def checkRegister(self, x):
        return x >= 0 and x < 4

instructions = [Instruction(x) for x in dir(Instruction) if x[0]!="_" and not(x in ["checkRegister", "execute"])]
print([i.name for i in instructions])

instructionsMap = [set() for x in instructions]
counter = 0
program = list()
with open("input.txt", "r") as file:
    line = file.readline()
    while line != "":
        if line.startswith("Before"):
            print(line, end="")
            registersBefore = list([int(x) for x in line[9:-2].split(",")])
            line = file.readline()
            print(line, end="")
            op = list([int(x) for x in line.split(" ")])
            line = file.readline()
            print(line, end="")
            registersAfter = list([int(x) for x in line[9:-2].split(",")])
            
            possibleInstructions = list()
            for instruction in instructions:
                cpu = list(registersBefore)
                if instruction.execute(cpu, op[1], op[2], op[3]) != False and cpu == registersAfter:
                    possibleInstructions.append(instruction)
                    
            print([i.name for i in possibleInstructions])
            if len(possibleInstructions) >= 3:
                counter+=1
            
            if len(instructionsMap[op[0]]) == 0:
                instructionsMap[op[0]] = set(possibleInstructions)
            else:
                instructionsMap[op[0]] & set(possibleInstructions)
        elif line.strip() != "":
            program.append(list([int(x) for x in line.split(" ")]))
        
        line = file.readline()
     
print(str(counter)+" behaves like 3 or more")
     
for opCode, possibleInstructions in enumerate(instructionsMap):
    print("Opcode: "+str(opCode)+" - "+str([i.name for i in possibleInstructions]))     
        
finalMap = [None for x in instructions]
wasChange = True
while wasChange:
    wasChange = False
    
    for opCode, possibleInstructions in enumerate(instructionsMap):
        if len(possibleInstructions) == 1:
            wasChange = True
            toRemove = list(possibleInstructions)[0]
            finalMap[opCode] = toRemove
            for iSet in instructionsMap:
                iSet.discard(toRemove)
            break;
        
for opCode, instruction in enumerate(finalMap):
    print("Opcode: "+str(opCode)+" - "+str(instruction.name if instruction != None else "None"))
    
print("Executing program")
cpu = [0, 0, 0, 0]
for op in program:
    print(op)
    finalMap[op[0]].execute(cpu, op[1], op[2], op[3])
    
print("Cpu state: "+str(cpu))