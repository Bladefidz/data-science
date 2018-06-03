import random, pylab
import numpy as np
from copy import copy

# Problem 3
def drawing_without_replacement_sim(numTrials):
	'''
	Runs numTrials trials of a Monte Carlo simulation
	of drawing 3 balls out of a bucket containing
	4 red and 4 green balls. Balls are not replaced once
	drawn. Returns a float - the fraction of times 3
	balls of the same color were drawn in the first 3 draws.
	'''
	bucket = [0, 0, 0, 1, 1, 1]
	random.shuffle(bucket)
	numTriple = 0
	for t in range(numTrials):
		sample = random.sample(bucket, 3)
		if (sum(sample) == 0 or sum(sample) == 3):
			numTriple += 1
	return numTriple/numTrials


# random.seed(0)
# numTrials = 1000
# prob = drawing_without_replacement_sim(numTrials)
# print('probability of triplet in {} trials is {}'.format(numTrials, prob))


# Problem 4
# You are given this function
def getMeanAndStd(X):
	mean = sum(X)/float(len(X))
	tot = 0.0
	for x in X:
		tot += (x - mean)**2
	std = (tot/len(X))**0.5
	return mean, std

# You are given this class
class Die(object):
	def __init__(self, valList):
		""" valList is not empty """
		self.possibleVals = valList[:]
	def roll(self):
		return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
	"""
	  - values, a sequence of numbers
	  - numBins, a positive int
	  - xLabel, yLabel, title, are strings
	  - Produces a histogram of values with numBins bins and the indicated
		labels for the x and y axis
	  - If title is provided by caller, puts that title on the figure and
		otherwise does not title the figure
	"""
	pylab.xlabel(xLabel)
	pylab.ylabel(yLabel)
	if title is not None:
		pylab.title(title)
	pylab.hist(values, numBins)
	pylab.show()


# Implement this -- Coding Part 2 of 2
def getAverage(die, numRolls, numTrials):
	"""
	  - die, a Die
	  - numRolls, numTrials, are positive ints
	  - Calculates the expected mean value of the longest run of a number
		over numTrials runs of numRolls rolls.
	  - Calls makeHistogram to produce a histogram of the longest runs for all
		the trials. There should be 10 bins in the histogram
	  - Choose appropriate labels for the x and y axes.
	  - Returns the mean calculated
	"""
	longestRuns = []  # Longest runs
	for trial in range(numTrials):
		sides = []
		for roll in range(numRolls):
			sides.append(die.roll())
		longestRun = 1
		for i in range(len(sides) - 1):
			j = i + 1
			while j < len(sides) and sides[j] == sides[i]:
				j += 1
			run = j - i
			if run > longestRun:
				longestRun = run
		longestRuns.append(longestRun)
	makeHistogram(longestRuns, 10, 'Longest Run', 'Frequency')
	return sum(longestRuns) / numTrials

# One test case
# print(getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000))

# # Test histogram for gaussian distribution
# mu, sigma = 100, 15
# x = mu + sigma * np.random.randn(10000)
# makeHistogram(x, 50, 'x', 'y')
# pylab.show()


# Problem 6
def find_combination(choices, total):
	"""
	choices: a non-empty list of ints
	total: a positive int

	Returns result, a numpy.array of length len(choices)
	such that
		* each element of result is 0 or 1
		* sum(result*choices) == total
		* sum(result) is as small as possible
	In case of ties, returns any result that works.
	If there is no result that gives the exact total,
	pick the one that gives sum(result*choices) closest
	to total without going over.
	"""
	result = np.zeros(len(choices))
	indexes = {}
	for i in range(len(choices)):
		c = choices[i]
		if c not in indexes:
			indexes[c] = [i]
		else:
			indexes[c].append(i)
	choices.sort(reverse=True)
	satisfiedVals = []
	currSum = 0
	for c in choices:
		if currSum + c < total:
			satisfiedVals.append(c)
			currSum += c
		elif currSum + c == total:
			satisfiedVals.append(c)
			currSum += c
			break
	for val in satisfiedVals:
		result[indexes[val].pop()] = 1
	return result


# print(find_combination([1,2,2,3], 4))
# print(find_combination([1,1,3,5,3], 5))
# print(find_combination([1,1,1,9], 4))


# Problem 8
# See rabbit.py