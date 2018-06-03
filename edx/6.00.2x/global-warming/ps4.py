import numpy as np
import matplotlib.pyplot as plt
import re
import itertools
import warnings
from numpy.linalg import inv

warnings.simplefilter('ignore', np.RankWarning)

# cities in our weather data
CITIES = [
	'BOSTON',
	'SEATTLE',
	'SAN DIEGO',
	'PHILADELPHIA',
	'PHOENIX',
	'LAS VEGAS',
	'CHARLOTTE',
	'DALLAS',
	'BALTIMORE',
	'SAN JUAN',
	'LOS ANGELES',
	'MIAMI',
	'NEW ORLEANS',
	'ALBUQUERQUE',
	'PORTLAND',
	'SAN FRANCISCO',
	'TAMPA',
	'NEW YORK',
	'DETROIT',
	'ST LOUIS',
	'CHICAGO'
]

INTERVAL_1 = list(range(1961, 2006))
INTERVAL_2 = list(range(2006, 2016))

"""
Begin helper code
"""
class Climate(object):
	"""
	The collection of temperature records loaded from given csv file
	"""
	def __init__(self, filename):
		"""
		Initialize a Climate instance, which stores the temperature records
		loaded from a given csv file specified by filename.

		Args:
			filename: name of the csv file (str)
		"""
		self.rawdata = {}

		f = open(filename, 'r')
		header = f.readline().strip().split(',')
		for line in f:
			items = line.strip().split(',')

			date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
			year = int(date.group(1))
			month = int(date.group(2))
			day = int(date.group(3))

			city = items[header.index('CITY')]
			temperature = float(items[header.index('TEMP')])
			if city not in self.rawdata:
				self.rawdata[city] = {}
			if year not in self.rawdata[city]:
				self.rawdata[city][year] = {}
			if month not in self.rawdata[city][year]:
				self.rawdata[city][year][month] = {}
			self.rawdata[city][year][month][day] = temperature

		f.close()

	def get_yearly_temp(self, city, year):
		"""
		Get the daily temperatures for the given year and city.

		Args:
			city: city name (str)
			year: the year to get the data for (int)

		Returns:
			a numpy 1-d array of daily temperatures for the specified year and
			city
		"""
		temperatures = []
		assert city in self.rawdata, "provided city is not available"
		assert year in self.rawdata[city], "provided year is not available"
		for month in range(1, 13):
			for day in range(1, 32):
				if day in self.rawdata[city][year][month]:
					temperatures.append(self.rawdata[city][year][month][day])
		return np.array(temperatures)

	def get_daily_temp(self, city, month, day, year):
		"""
		Get the daily temperature for the given city and time (year + date).

		Args:
			city: city name (str)
			month: the month to get the data for (int, where January = 1,
				December = 12)
			day: the day to get the data for (int, where 1st day of month = 1)
			year: the year to get the data for (int)

		Returns:
			a float of the daily temperature for the specified time (year +
			date) and city
		"""
		assert city in self.rawdata, "provided city is not available"
		assert year in self.rawdata[city], "provided year is not available"
		assert month in self.rawdata[city][year], "provided month is not available"
		assert day in self.rawdata[city][year][month], "provided day is not available"
		return self.rawdata[city][year][month][day]



"""
End helper code
"""

# Problem 1
def generate_models(x, y, degs):
	"""
	Generate regression models by fitting a polynomial for each degree in degs
	to points (x, y).
	Args:
		x: a list with length N, representing the x-coords of N sample points
		y: a list with length N, representing the y-coords of N sample points
		degs: a list of degrees of the fitting polynomial
	Returns:
		a list of numpy arrays, where each array is a 1-d array of coefficients
		that minimizes the squared error of the fitting polynomial
	"""
	x = np.asarray(x)
	degs = np.asarray(degs)
	maxdeg = max(degs)  # Max degree
	emax = maxdeg * 2  # Max exponent of X
	expX = np.zeros((emax-1, len(x)), dtype=np.int)  # [x^i, .., x^n] i=[2,.., n]
	expXY = np.zeros((maxdeg, len(x)))  # [x^i*y, ..] i=1

	# x0 = x[0]  # First value of x
	for i in range(len(x)):
		# x[i] -= x0  # Weighting each value of x by its initial value x0
		for j in range(emax-1):
			if j == 0:
				xe2 = x[i] ** 2
				expX[j][i] = xe2
				expXY[j][i] = y[i] * x[i]
				if maxdeg > 1:
					expXY[j+1][i] = y[i] * xe2
			else:
				expX[j][i] = expX[j-1][i] * x[i]
				if j < maxdeg-1:
					expXY[j+1][i] += y[i] * expX[j][i]

	sumx = np.zeros(emax+1, dtype=np.int)  # Sum of x^i, i=[0,..,n]
	sumx[0] = len(x)
	sumx[1] = sum(x)
	for i in range(emax-1):
		sumx[i+2] = expX[i].sum()

	sumxy = np.zeros(maxdeg+1)  # Sum of x^i*y, i=[n,..,0]
	sumxy[maxdeg] = sum(y)
	for i in range(maxdeg):
		sumxy[maxdeg-i-1] = expXY[i].sum()

	u = []
	for d in degs:
		r = d + 1  # Number of rows or coefficient
		a = np.zeros((r, r))
		ex = d*2  # Max exponent of x
		for i in range(r):
			for j in range(r):
				a[i][j] = sumx[ex-i-j]
		b = sumxy[len(sumxy)-r:len(sumxy)].reshape(r,1)
		u.append(np.matmul(np.linalg.inv(a), b))

	return u

def generate_models1(x, y, degs):
	x = np.asarray(x)
	y = np.asarray(y)
	u = []
	for d in degs:
		u.append(np.polyfit(x, y, d))
	return u

# Problem 2
def r_squared(y, estimated):
	"""
	Calculate the R-squared error term.
	Args:
		y: list with length N, representing the y-coords of N sample points
		estimated: a list of values estimated by the regression model
	Returns:
		a float for the R-squared error term
	"""
	error = ((estimated - y)**2).sum()
	meanError = error/len(y)
	return 1 - (meanError/np.var(y))

def horner(model, x):
	"""
	Return estimated y value for model equation using horner method
	Return:
		Array of estimated y
	"""
	y = np.zeros(len(x))
	i = 0
	for _x in x:
		y[i] = model[0]
		for m in model[1:len(model)]:
			y[i] = _x * y[i] + m
		i += 1
	return y

def get_model_label(model):
	"""
	Get label of model, eg: 5x^2+3x-1
	"""
	m = []
	e = len(model)-1
	for v in model:
		cx = round(float(v), 3)
		if cx >= 0 and e < len(model)-1:
			m.append('+')
		m.append(str(cx))
		if e > 0:
			m.append('x')
		if e > 1:
			m.append('^')
			m.append(str(e))
		e -= 1
	return ''.join(m)

# Problem 3
def evaluate_models_on_training(x, y, models):
	"""
	For each regression model, compute the R-square for this model with the
	standard error over slope of a linear regression line (only if the model is
	linear), and plot the data along with the best fit curve.

	For the plots, you should plot data points (x,y) as blue dots and your best
	fit curve (aka model) as a red solid line. You should also label the axes
	of this figure appropriately and have a title reporting the following
	information:
		degree of your regression model,
		R-square of your model evaluated on the given data points
	Args:
		x: a list of length N, representing the x-coords of N sample points
		y: a list of length N, representing the y-coords of N sample points
		models: a list containing the regression models you want to apply to
			your data. Each model is a numpy array storing the coefficients of
			a polynomial.
	Returns:
		None
	"""
	for m in models:
		esty = horner(m, x)
		error = r_squared(y, esty)
		plt.plot(x, y, 'bo', label = 'Data')
		plt.plot(x, esty, 'r-', label = 'f(x)')
		plt.legend(loc = 'best')
		t = []
		t.append('f(x): ')
		t.append(get_model_label(m))
		t.append('\n')
		t.append('R^2: ')
		t.append(str(round(error, 3)))
		plt.title(''.join(t))


### Begining of program
raw_data = Climate('data.csv')

# Problem 3
y = []
x = INTERVAL_1
for year in INTERVAL_1:
	y.append(raw_data.get_daily_temp('BOSTON', 1, 10, year))
models = generate_models(x, y, [1])
evaluate_models_on_training(x, y, models)
plt.show()

# Problem 4: FILL IN MISSING CODE TO GENERATE y VALUES
x1 = INTERVAL_1
x2 = INTERVAL_2
y = []
for year in INTERVAL_1:
	y.append(np.mean(raw_data.get_yearly_temp('BOSTON', year)))
models = generate_models(x1, y, [1])
# models = generate_models1(x1, y, [1])
evaluate_models_on_training(x1, y, models)
plt.show()
