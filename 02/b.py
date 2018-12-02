def difference(first, second):
	differencies = list()
	for i in range(len(first)):
		if first[i] != second[i]:
			differencies.append(i)
	return differencies

ids = list()

with open("input.txt", "r") as lines:
	for line in lines:
		ids.append(line)
		
for id in ids:
	for id2 in ids:
		diff = difference(id, id2)
		if len(diff) == 1:
			print(id[:diff[0]]+id[diff[0]+1:])