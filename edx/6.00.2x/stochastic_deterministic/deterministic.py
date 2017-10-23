import random

# Code Sample A
mylist = []

'''
	Deterministic, because will always produce [7]. Look at line 17.
'''
for i in range(random.randint(1, 10)):
    random.seed(0)
    if random.randint(1, 10) > 3:
        number = random.randint(1, 10)
        if number not in mylist:
            mylist.append(number)
print(mylist)

# Code Sample B
mylist = []

'''
	Deterministic, because will always produce [1, 9, 7, 8, 10, 9].
'''
random.seed(0)
for i in range(random.randint(1, 10)):
    if random.randint(1, 10) > 3:
        number = random.randint(1, 10)
        mylist.append(number)
    print(mylist)