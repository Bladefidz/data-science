import random

def noReplacementSimulation(numTrials):
	'''
	Runs numTrials trials of a Monte Carlo simulation
	of drawing 3 balls out of a bucket containing
	3 red and 3 green balls. Balls are not replaced once
	drawn. Returns the a decimal - the fraction of times 3
	balls of the same color were drawn.
	'''
	p3 = 0
	for t in range(numTrials):
		draw = 3
		balls = [1, 2, 3, 4, 5, 6]
		color = -1
		color3 = True
		for d in range(draw):
			got = random.choice(balls)
			if color == -1:
				color = got % 2
			elif color != got % 2:
				color3 = False
				break
			ig = balls.index(got)
			balls = balls[0:ig] + balls[ig+1:len(balls)]
		if color3:
			p3 += 1
	return p3 / numTrials


if __name__ == '__main__':
	print("# Test 1")
	p = noReplacementSimulation(5000)
	print("Expected a value between 0.088 and 0.112; got", p)
	if p >= 0.088 and p <= 0.111:
		print("True")
	else:
		print("False")

	print("# Test 2")
	p = []
	for i in range(5):
		p.append(noReplacementSimulation(5000))
	print("Expected a value between 0.088 and 0.112; got", p)
	r = True
	for q in p:
		if q < 0.088 or q > 0.111:
			r = False
			break
	print(r)