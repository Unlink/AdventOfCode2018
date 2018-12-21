class Instruction:
    def __init__(self, name):
        if not(name in dir(self)):
            raise Exception("Instruction not exists")
        self.name = name
        
    def executeArry(self, cpu, params):
        self.execute(cpu,params[0], params[1], params[2])
        
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
        return x >= 0 and x < 6

program = list()
ipr = 0
with open("input.txt", "r") as file:
    ipr = int(file.readline().replace("#ip ", ""))
    line = file.readline()
    while line != "":
        instructionInfo = line.split(" ")
        program.append((Instruction(instructionInfo[0]), [int(instructionInfo[i+1]) for i in range(3)]))
        line = file.readline()
    
print("Executing program")

cpu = [0, 0, 0, 0, 0, 0]
ip = 0
r0Values = list()

while ip >= 0 and ip < len(program):
    cpu[ipr] = ip
    program[ip][0].executeArry(cpu, program[ip][1])
    #print(program[ip][0].name + " " + " ".join([str(x) for x in program[ip][1]]) + "\t" + str(cpu))
    ip = cpu[ipr]
    ip += 1
    if ip == 28:
        if cpu[5] in r0Values:
            print(r0Values)
            print(cpu[5])
            break
        r0Values.append(cpu[5])
        print(str(len(r0Values))+":"+str(cpu[5]))
print("Cpu state: "+str(cpu))