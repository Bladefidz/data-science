from ps3b_precompiled_36 import *
import random
import numpy as np

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb,
	resistances, mutProb, numTrials):
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
	viruses = []
	for i in range(numViruses):
		viruses.append(
			ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

	# Prepare samples
	s1 = []  # Sample of all viruses
	s2 = []  # Sample of resistances viruses
	for i in range(300):
		s1.append([])
		s2.append([])

	# Run simulation and get the samples
	for t in range(numTrials):
		patient = TreatedPatient(viruses, maxPop)
		for s in range(150):
			s1[s].append(patient.update())
			s2[s].append(0.0)
		patient.addPrescription('guttagonol')
		for s in range(150, 300):
			s1[s].append(patient.update())
			s2[s].append(patient.getResistPop('guttagonol'))

	# Calculate average of each samples
	avgs1 = []
	for s in s1:
		avgs1.append(sum(s)/float(numTrials))
	s1 = None
	avgs2 = []
	for s in s2:
		avgs2.append(sum(s)/float(numTrials))
	s2 = None

	# Returning all average samples
	return s1, s2

def plot(sampleTuple):
	pylab.plot(sampleTuple[0], label = "Total Virus Population")
	pylab.plot(sampleTuple[1], label = "Total Resistance Virus Population")
	pylab.title("ResistantVirus simulation")
	pylab.xlabel("Time Steps")
	pylab.ylabel("Average Virus Population")
	pylab.legend(loc = "best")
	pylab.show()

# plot(simulationWithoutDrug(1, 10, 1.0, 0.0, 1))
# plot(simulationWithoutDrug(100, 200, 0.2, 0.8, 1))
# plot(simulationWithoutDrug(1, 90, 0.8, 0.1, 1))
plot(simulationWithDrug(
	100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 100))