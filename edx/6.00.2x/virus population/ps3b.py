# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics

import random
import pylab

'''
Begin helper code
'''

class NoChildException(Exception):
	"""
	NoChildException is raised by the reproduce() method in the SimpleVirus
	and ResistantVirus classes to indicate that a virus particle does not
	reproduce. You can use NoChildException as is, you do not need to
	modify/add any code.
	"""
	pass

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):
	"""
	Representation of a simple virus (does not model drug effects/resistance).
	"""
	def __init__(self, maxBirthProb, clearProb):
		"""
		Initialize a SimpleVirus instance, saves all parameters as attributes
		of the instance.
		maxBirthProb: Maximum reproduction probability (a float between 0-1)
		clearProb: Maximum clearance probability (a float between 0-1).
		"""
		self.maxBirthProb = maxBirthProb
		self.clearProb = clearProb
		self.prob = 0

	def getMaxBirthProb(self):
		"""
		Returns the max birth probability.
		"""
		return self.maxBirthProb

	def getClearProb(self):
		"""
		Returns the clear probability.
		"""
		return self.clearProb

	def doesClear(self):
		""" Stochastically determines whether this virus particle is cleared from the
		patient's body at a time step.
		returns: True with probability self.getClearProb and otherwise returns
		False.
		"""
		if self.clearProb == 1:
			return True
		if self.clearProb == 0:
			return False
		self.prob = random.random()
		if self.prob <= self.clearProb:
			return True
		return False

	def reproduce(self, popDensity):
		"""
		Stochastically determines whether this virus particle reproduces at a
		time step. Called by the update() method in the Patient and
		TreatedPatient classes. The virus particle reproduces with probability
		self.maxBirthProb * (1 - popDensity).

		If this virus particle reproduces, then reproduce() creates and returns
		the instance of the offspring SimpleVirus (which has the same
		maxBirthProb and clearProb values as its parent).

		popDensity: the population density (a float), defined as the current
		virus population divided by the maximum population.

		returns: a new instance of the SimpleVirus class representing the
		offspring of this virus particle. The child should have the same
		maxBirthProb and clearProb values as this virus. Raises a
		NoChildException if this virus particle does not reproduce.
		"""
		pReprd = self.maxBirthProb * (1 - popDensity)
		if pReprd == 0 and self.prob <= pReprd:
			raise NoChildException
		return SimpleVirus(self.maxBirthProb, self.clearProb)


class Patient(object):
	"""
	Representation of a simplified patient. The patient does not take any drugs
	and his/her virus populations have no drug resistance.
	"""
	def __init__(self, viruses, maxPop):
		"""
		Initialization function, saves the viruses and maxPop parameters as
		attributes.

		viruses: the list representing the virus population (a list of
		SimpleVirus instances)

		maxPop: the maximum virus population for this patient (an integer)
		"""
		self.viruses = viruses
		self.maxPop = maxPop
		self.popDensity = len(viruses)/maxPop

	def getViruses(self):
		"""
		Returns the viruses in this Patient.
		"""
		return self.viruses

	def getMaxPop(self):
		"""
		Returns the max population.
		"""
		return self.maxPop

	def getTotalPop(self):
		"""
		Gets the size of the current total virus population.
		returns: The total virus population (an integer)
		"""
		return len(self.viruses)

	def update(self):
		"""
		Update the state of the virus population in this patient for a single
		time step. update() should execute the following steps in this order:

		- Determine whether each virus particle survives and updates the list
		of virus particles accordingly.

		- The current population density is calculated. This population density
		  value is used until the next call to update()

		- Based on this value of population density, determine whether each
		  virus particle should reproduce and add offspring virus particles to
		  the list of viruses in this patient.

		returns: The total virus population at the end of the update (an
		integer)
		"""
		if self.popDensity > 0 and self.popDensity < 1:
			try:
				survived = []
				for virus in self.viruses:
					if virus.doesClear() is False:
						survived.append(virus)
				self.viruses = survived
				nextPopDensity = len(self.viruses) / self.maxPop
				child = []
				for virus in self.viruses:
					child.append(virus.reproduce(self.popDensity))
				self.viruses += child
				self.popDensity = nextPopDensity
			except NoChildException:
				pass
		return len(self.viruses)

print("#Test 1: Initialize a SimpleVirus that is never cleared and always reproduces")
v1 = SimpleVirus(1.0, 0.0)
tp = False
for x in range(10):
	tp = v1.doesClear()
	if tp: break
print(tp == False)
print("#Test 2: Initialize a SimpleVirus that is never cleared and never reproduces")
v1 = SimpleVirus(0.0, 0.0)
tp = False
for x in range(10):
	tp = v1.doesClear()
	if tp: break
print(tp == False)
print("#Test 3: Initialize a SimpleVirus that is always cleared and always reproduces")
v1 = SimpleVirus(1.0, 1.0)
tp = True
for x in range(10):
	tp = v1.doesClear()
	if tp is False: break
print(tp == True)
print("#Test 4: Initialize a SimpleVirus that is always cleared and never reproduces")
v1 = SimpleVirus(0.0, 1.0)
tp = True
for x in range(10):
	tp = v1.doesClear()
	if tp is False: break
print(tp == True)
print("#Test 5: Initialize a SimpleVirus with randomized probabilities")
v1 = SimpleVirus(0.95, 0.87)
popDensity = 0.01
print("Pop Density", popDensity)
tp = True
for i in range(10):
	try:
		v1.reproduce(popDensity)
	except NoChildException:
		tp = False
		break
print(tp)
print("#Test 6: Initialize a Patient with randomized viruses")
viruses = [SimpleVirus(0.45, 0.68), SimpleVirus(0.31, 0.0),
	SimpleVirus(0.17, 0.0), SimpleVirus(0.32, 0.88)]
P1 = Patient(viruses, 7)
tp = P1.getTotalPop()
if tp == 4: print(True)
else: print(False, "-Expectation t=4, got", tp)
print("#Test 7: Create a Patient with virus that is never cleared and always reproduces")
virus = SimpleVirus(1.0, 0.0)
patient = Patient([virus], 100)
for i in range(100):
	patient.update()
tp = patient.getTotalPop()
print("Expected >= 100")
if tp >= 100: print(True)
else: print(False, tp)
print("#Test 8: Create a Patient with virus that is always cleared and always reproduces")
virus = SimpleVirus(1.0, 1.0)
patient = Patient([virus], 100)
for i in range(100):
	patient.update()
tp = patient.getTotalPop()
print("Expected = 0")
if tp == 0: print(True)
else: print(False, tp)
print("#Test 9: Initialize a Patient with randomized viruses")
viruses = [SimpleVirus(0.91, 0.9500000000000001), SimpleVirus(0.39, 0.84),
	SimpleVirus(0.07, 0.8200000000000001)]
patient = Patient(viruses, 9)
tp = patient.getTotalPop()
print("Expected = 3")
if tp == 3: print(True)
else: print(False, tp)
tp = True
for i in range(10):
	patient.update()
	if len(patient.viruses) >= patient.maxPop: tp = False; break;
print("Expected True")
print(tp)
print("#Test 10: Check exception handling by raising different types of exceptions in SimpleVirus.reproduce")
virus = SimpleVirus(1.0, 1.0)
patient = Patient(viruses, 9)


#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
						  numTrials):
	"""
	Run the simulation and plot the graph for problem 3 (no drugs are used,
	viruses do not have any drug resistance).
	For each of numTrials trial, instantiates a patient, runs a simulation
	for 300 timesteps, and plots the average virus population size as a
	function of time.

	numViruses: number of SimpleVirus to create for patient (an integer)
	maxPop: maximum virus population for patient (an integer)
	maxBirthProb: Maximum reproduction probability (a float between 0-1)
	clearProb: Maximum clearance probability (a float between 0-1)
	numTrials: number of simulation runs to execute (an integer)
	"""

	# TODO



#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
	"""
	Representation of a virus which can have drug resistance.
	"""

	def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
		"""
		Initialize a ResistantVirus instance, saves all parameters as attributes
		of the instance.

		maxBirthProb: Maximum reproduction probability (a float between 0-1)

		clearProb: Maximum clearance probability (a float between 0-1).

		resistances: A dictionary of drug names (strings) mapping to the state
		of this virus particle's resistance (either True or False) to each drug.
		e.g. {'guttagonol':False, 'srinol':False}, means that this virus
		particle is resistant to neither guttagonol nor srinol.

		mutProb: Mutation probability for this virus particle (a float). This is
		the probability of the offspring acquiring or losing resistance to a drug.
		"""

		# TODO


	def getResistances(self):
		"""
		Returns the resistances for this virus.
		"""
		# TODO

	def getMutProb(self):
		"""
		Returns the mutation probability for this virus.
		"""
		# TODO

	def isResistantTo(self, drug):
		"""
		Get the state of this virus particle's resistance to a drug. This method
		is called by getResistPop() in TreatedPatient to determine how many virus
		particles have resistance to a drug.

		drug: The drug (a string)

		returns: True if this virus instance is resistant to the drug, False
		otherwise.
		"""

		# TODO


	def reproduce(self, popDensity, activeDrugs):
		"""
		Stochastically determines whether this virus particle reproduces at a
		time step. Called by the update() method in the TreatedPatient class.

		A virus particle will only reproduce if it is resistant to ALL the drugs
		in the activeDrugs list. For example, if there are 2 drugs in the
		activeDrugs list, and the virus particle is resistant to 1 or no drugs,
		then it will NOT reproduce.

		Hence, if the virus is resistant to all drugs
		in activeDrugs, then the virus reproduces with probability:

		self.maxBirthProb * (1 - popDensity).

		If this virus particle reproduces, then reproduce() creates and returns
		the instance of the offspring ResistantVirus (which has the same
		maxBirthProb and clearProb values as its parent). The offspring virus
		will have the same maxBirthProb, clearProb, and mutProb as the parent.

		For each drug resistance trait of the virus (i.e. each key of
		self.resistances), the offspring has probability 1-mutProb of
		inheriting that resistance trait from the parent, and probability
		mutProb of switching that resistance trait in the offspring.

		For example, if a virus particle is resistant to guttagonol but not
		srinol, and self.mutProb is 0.1, then there is a 10% chance that
		that the offspring will lose resistance to guttagonol and a 90%
		chance that the offspring will be resistant to guttagonol.
		There is also a 10% chance that the offspring will gain resistance to
		srinol and a 90% chance that the offspring will not be resistant to
		srinol.

		popDensity: the population density (a float), defined as the current
		virus population divided by the maximum population

		activeDrugs: a list of the drug names acting on this virus particle
		(a list of strings).

		returns: a new instance of the ResistantVirus class representing the
		offspring of this virus particle. The child should have the same
		maxBirthProb and clearProb values as this virus. Raises a
		NoChildException if this virus particle does not reproduce.
		"""

		# TODO



class TreatedPatient(Patient):
	"""
	Representation of a patient. The patient is able to take drugs and his/her
	virus population can acquire resistance to the drugs he/she takes.
	"""

	def __init__(self, viruses, maxPop):
		"""
		Initialization function, saves the viruses and maxPop parameters as
		attributes. Also initializes the list of drugs being administered
		(which should initially include no drugs).

		viruses: The list representing the virus population (a list of
		virus instances)

		maxPop: The  maximum virus population for this patient (an integer)
		"""

		# TODO


	def addPrescription(self, newDrug):
		"""
		Administer a drug to this patient. After a prescription is added, the
		drug acts on the virus population for all subsequent time steps. If the
		newDrug is already prescribed to this patient, the method has no effect.

		newDrug: The name of the drug to administer to the patient (a string).

		postcondition: The list of drugs being administered to a patient is updated
		"""

		# TODO


	def getPrescriptions(self):
		"""
		Returns the drugs that are being administered to this patient.

		returns: The list of drug names (strings) being administered to this
		patient.
		"""

		# TODO


	def getResistPop(self, drugResist):
		"""
		Get the population of virus particles resistant to the drugs listed in
		drugResist.

		drugResist: Which drug resistances to include in the population (a list
		of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

		returns: The population of viruses (an integer) with resistances to all
		drugs in the drugResist list.
		"""

		# TODO


	def update(self):
		"""
		Update the state of the virus population in this patient for a single
		time step. update() should execute these actions in order:

		- Determine whether each virus particle survives and update the list of
		  virus particles accordingly

		- The current population density is calculated. This population density
		  value is used until the next call to update().

		- Based on this value of population density, determine whether each
		  virus particle should reproduce and add offspring virus particles to
		  the list of viruses in this patient.
		  The list of drugs being administered should be accounted for in the
		  determination of whether each virus particle reproduces.

		returns: The total virus population at the end of the update (an
		integer)
		"""

		# TODO



#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
					   mutProb, numTrials):
	"""
	Runs simulations and plots graphs for problem 5.

	For each of numTrials trials, instantiates a patient, runs a simulation for
	150 timesteps, adds guttagonol, and runs the simulation for an additional
	150 timesteps.  At the end plots the average virus population size
	(for both the total virus population and the guttagonol-resistant virus
	population) as a function of time.

	numViruses: number of ResistantVirus to create for patient (an integer)
	maxPop: maximum virus population for patient (an integer)
	maxBirthProb: Maximum reproduction probability (a float between 0-1)
	clearProb: maximum clearance probability (a float between 0-1)
	resistances: a dictionary of drugs that each ResistantVirus is resistant to
				 (e.g., {'guttagonol': False})
	mutProb: mutation probability for each ResistantVirus particle
			 (a float between 0-1).
	numTrials: number of simulation runs to execute (an integer)

	"""

	# TODO
