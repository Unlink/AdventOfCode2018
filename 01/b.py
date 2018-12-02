changes = list()
with open("input.txt", "r") as lines:
	for line in lines:
		if line[0] == '+':
			changes.append(int(line[1:]))
		elif line[0] == '-':
			changes.append(-int(line[1:]))

sum = 0
frequenturies = set()
frequenturies.add(sum)

while True:
	for change in changes:
		sum += change
		if (sum in frequenturies):
			print(sum)
			exit()
		else:
			frequenturies.add(sum)