input = 909441

scoreBoard = [3,7]

a = 0
b = 1

while len(scoreBoard) < (input + 10):
    sum = scoreBoard[a] + scoreBoard[b]
    if sum > 9:
        scoreBoard.append(1)#sum/10
    scoreBoard.append(sum%10)
    
    a = (a + (scoreBoard[a] + 1)) % len(scoreBoard)
    b = (b + (scoreBoard[b] + 1)) % len(scoreBoard)
    
    #for i in scoreBoard:
    #    print(i, end=" ")
    #print()

for i in range(len(scoreBoard)-10, len(scoreBoard)):
    print(scoreBoard[i], end="")
    
print()