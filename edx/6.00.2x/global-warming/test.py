import numpy as np
import pylab
import re
import warnings
import itertools
from time import time

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

def generate_models(x, y, degs):
	x = np.asarray(x)
	degs = np.asarray(degs)
	maxdeg = max(degs)  # Max degree
	emax = maxdeg * 2  # Max exponent of X
	expX = np.zeros((emax-1, len(x)), dtype=np.int)  # [x^i, .., x^n] i=[2,.., n]
	expXY = np.zeros((maxdeg, len(x)))  # [x^i*y, ..] i=1

	x0 = x[0]  # First value of x
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

# x = [0, 1, 3, 4]
# y = [1, 9, 9, 21]
# degs = [d for d in range(1, 300)]
# x = [1961, 1962, 1963]
# x = [1, 2, 3]
# y = [4.4, 5.5, 6.6]
# degs = [1, 2]

# print('x', x)
# print('y', y)
# print('degrees', degs)
# u = generate_models(x, y, degs)
# for i in range(len(degs)):
# 	print(degs[i], u[i])

# # Benchmarking
# t = time()
# generate_models(x, y, degs)
# print('me', time()-t)
# t = time()
# generate_models1(x, y, degs)
# print('np', time()-t)

def r_squared(y, estimated):
	y = np.asarray(y)
	estimated = np.asarray(estimated)
	meany = y.sum()/len(y)
	sumye2 = 0
	sumymean2 = 0
	for _y, _e in itertools.zip_longest(y, estimated):
		ye2 = _y**2
		_2y = 2*_y
		sumye2 += ye2 - _2y*_e + _e**2
		sumymean2 += ye2 - _2y*meany + meany**2
	return 1 - sumye2 / sumymean2

def rSquared1(observed, predicted):
    error = ((predicted - observed)**2).sum()
    meanError = error/len(observed)
    return 1 - (meanError/np.var(observed))

# y = np.asarray([i for i in range(10000)])
# est = np.asarray([i for i in range(5, 10000+5)])
# # print(len(y))
# # print(len(est))
# t = time()
# r_squared(y, est)
# print("My r_squared:", time()-t)
# t = time()
# rSquared1(y, est)
# print("Guttag's r_squared:", time()-t)


def horner(model, x):
	y = np.zeros(len(x))
	i = 0
	for _x in x:
		y[i] = model[0]
		for m in model[1:len(model)]:
			y[i] = _x * y[i] + m
		i += 1
	return y

# x = [1.0, 2.0, 3.0, 4.0]
# models = []
# for i in range(2, 500):
# 	models.append(np.array([j for j in range(1, i+1)]))
# # print(models)
# for m in models:
# 	print(horner(m, x) == np.polyval(m, x))

# # Benchmark
# t = time()
# for m in models:
# 	horner(m, x)
# print("My horner:", time()-t)
# t = time()
# for m in models:
# 	np.polyval(m, x)
# print("Numpy horner:", time()-t)

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

def evaluate_models_on_training(x, y, models):
	for m in models:
		esty = horner(m, x)
		error = r_squared(y, esty)
		pylab.plot(x, y, 'bo', label = 'Data')
		pylab.plot(x, esty, 'r-', label = 'f(x)')
		pylab.legend(loc = 'best')
		t = []
		t.append('f(x): ')
		t.append(get_model_label(m))
		t.append('\n')
		t.append('R^2: ')
		t.append(str(round(error, 3)))
		pylab.title(''.join(t))


### Begining of program
raw_data = Climate('data.csv')

# Problem 3
y = []
x = INTERVAL_1
for year in INTERVAL_1:
	y.append(raw_data.get_daily_temp('BOSTON', 1, 10, year))
models = generate_models(x, y, [1])
# models = generate_models1(x, y, [1])
pylab.figure("Daily temperature: BOSTON 10 January")
evaluate_models_on_training(x, y, models)

# Problem 4: FILL IN MISSING CODE TO GENERATE y VALUES
x1 = INTERVAL_1
x2 = INTERVAL_2
y = []
for year in INTERVAL_1:
	y.append(np.mean(raw_data.get_yearly_temp('BOSTON', year)))
models = generate_models(x1, y, [1])
# models = generate_models1(x1, y, [1])
pylab.figure("Daily temperature: BOSTON yearly")
evaluate_models_on_training(x1, y, models)

pylab.show()