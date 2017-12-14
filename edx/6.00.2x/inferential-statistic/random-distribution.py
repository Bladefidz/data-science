import math
import matplotlib.pyplot as plt

def fact(x, y):
	if x == y:
		return y
	return x * fact(x-1, y)


# Plot distribution
plt.scatter(x, y)
x = np.array([min(x), max(x)])
plt.plot(x, f(x), label='Regression line')
plt.legend()
plt.show()


if __name__ == '__main__':
	print(fact(9, 6))