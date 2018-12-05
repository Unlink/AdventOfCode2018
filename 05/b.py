from string import ascii_lowercase

class Node:
    
    def __init__(self, char):
        self.c = char
        self.next = None
        
    def tryToAnihilate(self):
        if self.c.islower() and self.c.upper() == self.next.c:
            return self.next.next
        elif self.c.isupper() and self.c.lower() == self.next.c:
            return self.next.next
        else:
            return None
            
def printChain(node):
    current = node
    while current != None:
        print(current)
        current = current.next
        
def countChain(node):
    size = 0
    current = node
    while current != None:
        size+=1
        current = current.next
    return size 

file = open("input.txt", "r")
chain = file.read()
min = 100000000000

for toRemove in ascii_lowercase:
    testChain = chain.replace(toRemove, "").replace(toRemove.upper(), "")

    head = Node("")
    prev = head
    for c in testChain:
        node = Node(c)
        prev.next = node
        prev = node

    head = head.next

    stack = list()
    stack.append(head)

    while len(stack) > 0 and stack[len(stack)-1].next != None:
        current = stack[len(stack)-1]
        next = current.tryToAnihilate()
        
        if next == None:
            stack.append(current.next)
        else:
            stack.pop()
            if len(stack) == 0:
                stack.append(next)
            else:
                stack[len(stack)-1].next = next
                
    print(toRemove + ": " + str(countChain(stack[0])))
    if countChain(stack[0]) < min:
        min = countChain(stack[0])
        
print(min)

