import random
mylist = []

'''
	This is stochastic, because the size of list will always varies, while
	value of list always contains 7.
'''
for i in range(random.randint(1, 10)):
    random.seed(0)
    if random.randint(1, 10) > 3:
        number = random.randint(1, 10)
        mylist.append(number)
print(mylist)