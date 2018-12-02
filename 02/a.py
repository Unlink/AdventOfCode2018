def countLetters(line):
	counter = dict()
	twos = 0
	threes = 0
	for c in line:
		if c in counter:
			counter[c] += 1
		else:
			counter[c] = 1
			
	for c in counter:
		if counter[c] == 2:
			twos+=1
		if counter[c] == 3:
			threes+=1
	
	return (min(twos, 1), min(threes, 1))

twos = 0
threes = 0
	
with open("input.txt", "r") as lines:
	for line in lines:
		a, b = countLetters(line)
		twos += a
		threes += b
		
print(twos*threes)