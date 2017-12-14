def max_contig_sum(L):
	""" L, a list of integers, at least one positive
	Returns the maximum sum of a contiguous subsequence in L """
	s = 0
	for l in L:
		if l > s:
			s = l
	for i in range(len(L)):
		if i < len(L) - 1:
			r = sum(L[i:len(L)])
			if r > s:
				s = r
		if i > 0:
			r = sum(L[0:len(L) - i])
			if r > s:
				s = r
	return s

# if __name__ == '__main__':
# 	# [3, 4, -1, 5, -4], the maximum sum is 3+4-1+5 = 11
# 	print(max_contig_sum([3, 4, -1, 5, -4]) == 11)

# 	# [3, 4, -8, 15, -1, 2], the maximum sum is 15-1+2 = 16
# 	print(max_contig_sum([3, 4, -8, 15, -1, 2]) == 16)