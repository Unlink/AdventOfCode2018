class Marble:
    
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        
    def setLeft(self, left):
        self.left = left
        
    def setRight(self, right):
        self.right = right
        
    def insertAfter(self, marble):
        self.right.left = marble
        marble.right = self.right
        self.right = marble
        marble.left = self
    def remove(self):
        self.left.right = self.right
        self.right.left = self.left

        
players = 446 
marbles = 71522

playerScores = [0 for i in range(players)]
playerIndex = 0

#first marbles
current = Marble(0)
current.setLeft(current)
current.setRight(current)

for num in range(1,marbles+1):
    if num % 23 == 0:
        playerScores[playerIndex] += num
        toRemove = current
        for i in range(7):
            toRemove = toRemove.left
        playerScores[playerIndex] += toRemove.value
        current = toRemove.right
        toRemove.remove()
        
    else:
        newMarble = Marble(num)
        current.right.insertAfter(newMarble)
        current = newMarble
    playerIndex = (playerIndex + 1)%players
    
print(max(playerScores))