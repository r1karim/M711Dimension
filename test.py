word = input("Enter a string-> ")

for index in range(len(word)):
	if(index % 4 == 0 or index % 4==1):
		print(word[index].upper(), end='')
	else:
		print(word[index],end='')