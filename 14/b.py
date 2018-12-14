input = "909441"

inputAry = [int(i) for i in str(input)]
print(inputAry)
scoreBoard = [3,7]

a = 0
b = 1

while True:
    sum = scoreBoard[a] + scoreBoard[b]
    if sum > 9:
        scoreBoard.append(1)#sum/10
    scoreBoard.append(sum%10)
    
    a = (a + (scoreBoard[a] + 1)) % len(scoreBoard)
    b = (b + (scoreBoard[b] + 1)) % len(scoreBoard)
    
    #for i in scoreBoard:
    #    print(i, end=" ")
    #print()
    if len(scoreBoard) > len(inputAry)+1:
        for i in range(len(inputAry)):
            if not(inputAry[i] == scoreBoard[len(scoreBoard) - len(inputAry) + i]):
                break
        else:
            print(len(scoreBoard) - len(inputAry))
            break
            
        for i in range(len(inputAry)):
            if not(inputAry[i] == scoreBoard[len(scoreBoard) - len(inputAry) + i - 1]):
                break
        else:
            print(len(scoreBoard) - len(inputAry) - 1)
            break