
sum = 0

with open("input.txt", "r") as lines:
	for line in lines:
		if line[0] == '+':
			print(str(sum)+" + "+line[1:])
			sum += int(line[1:])
		elif line[0] == '-':
			print(str(sum)+" - "+line[1:])
			sum -= int(line[1:])
			
			
print(sum)