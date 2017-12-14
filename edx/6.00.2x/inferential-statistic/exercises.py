import math

def stdDevOfLengths(L):
	"""
	L: a list of strings

	returns: float, the standard deviation of the lengths of the strings,
	  or NaN if L is empty.
	"""
	if len(L) == 0:
		return float('NaN')

	s = 0
	for l in L:
		s += len(l)

	mean = s / len(L)

	s = 0
	for l in L:
		s += (len(l) - mean)**2

	return math.sqrt(s/len(L))

def coefVar(L):
	"""
	L: a list of ints
	returns: float, coefficient of variance
	"""
	if len(L) == 0:
		return float('NaN')

	s = 0
	for l in L:
		s += l

	mean = s / len(L)

	s = 0
	for l in L:
		s += (l - mean)**2

	return math.sqrt(s / len(L)) / mean

if __name__ == '__main__':
	# print(stdDevOfLengths(['a', 'z', 'p']) == 0)
	# print(stdDevOfLengths(['apples', 'oranges', 'kiwis', 'pineapples']) == 1.8708286933869707)
	print(coefVar([10, 4, 12, 15, 20, 5]))