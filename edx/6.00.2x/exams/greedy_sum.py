def greedySum(L, s):
	""" input: s, positive integer, what the sum should add up to
			   L, list of unique positive integers sorted in descending order
		Use the greedy approach where you find the largest multiplier for
		the largest value in L then for the second largest, and so on to
		solve the equation s = L[0]*m_0 + L[1]*m_1 + ... + L[n-1]*m_(n-1)
		return: the sum of the multipliers or "no solution" if greedy approach
				does not yield a set of multipliers such that the equation
				sums to 's'
	"""
	sm = 0
	r = 0
	for i in range(len(L)):
		if L[i] > s:
			continue
		t = s - r
		if i < len(L) - 1:
			t -= sum(L[i+1:])
		t = int(t / L[i])  # Floor
		if t == 0:
			if r + L[i] > s:
				continue
			t = 1
		sm += t
		r += L[i] * t
	if r != s:
		return "no solution"
	return sm

# if __name__ == '__main__':
# 	# Unit testing
# 	print(greedySum([], 10) == "no solution")
# 	print(greedySum([1], 20) == 20)
# 	print(greedySum([10, 5, 1], 14) == 5)
# 	print(greedySum([10, 5, 1], 11) == 2)
# 	print(greedySum([10, 9, 8, 1], 20) == 2)  #2
# 	print(greedySum([10, 9, 8, 1], 17) == 8)
# 	print(greedySum([10, 8, 5, 1], 13) == 4)
# 	print(greedySum([15, 12, 4, 3, 1], 29) == 4)
# 	print(greedySum([16, 12, 5, 3, 1], 15) == 2)
# 	print(greedySum([16, 12, 5, 3, 1], 24) == 3)
# 	print(greedySum([10, 7, 6, 3], 19) == "no solution")
# 	print(greedySum([10, 8, 5, 2], 16) == "no solution")
# 	print(greedySum([11, 10, 8, 5, 1], 16) == 2)
# 	print(greedySum([12, 10, 8, 5, 2], 17) == 2)
# 	print(greedySum([20, 10, 4, 3, 1], 21) == 2)
# 	print(greedySum([21, 10, 8, 3, 1], 11) == 2)
# 	print(greedySum([30, 20, 10], 60) == 3)
# 	print(greedySum([50, 25, 5], 5) == 1)
# 	print(greedySum([101, 51, 11, 2, 1], 3000) == 36)