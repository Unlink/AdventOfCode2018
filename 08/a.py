class Node:
    
    def __init__(self, nChnildrens, nMetaData):
        self.nChnildrens = nChnildrens
        self.nMetaData = nMetaData
        self.childrens = list()
        self.metaData = list()
        
    def hasAllChildrens(self):
        return len(self.childrens) == self.nChnildrens

input = list()
        
with open("input.txt", "r") as file:
    input = [int(n) for n in file.read().strip().split()]
    
treeStack = list()

head = Node(input.pop(0), input.pop(0))
treeStack.append(head)

while len(treeStack) > 0:
    node = treeStack.pop()
    if node.hasAllChildrens():
        for i in range(node.nMetaData):
            node.metaData.append(input.pop(0))
    else:
        treeStack.append(node)
        children = Node(input.pop(0), input.pop(0))
        node.childrens.append(children)
        treeStack.append(children)
        
        
checksum = 0

stack = list()
stack.append(head)

while len(stack) > 0:
    node = stack.pop()
    checksum += sum(node.metaData)
    stack += node.childrens
        
print(checksum)