from ps3b_precompiled_36 import *
import random
import numpy as np

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
	viruses = []
	for i in range(numViruses):
		viruses.append(SimpleVirus(maxBirthProb, clearProb))
	samples = []
	for i in range(300):
		samples.append([])
	for t in range(numTrials):
		patient = Patient(viruses, maxPop)
		for s in range(300):
			samples[s].append(patient.update())
	avgSample = []
	for s in samples:
		avgSample.append(sum(s)/float(numTrials))
	samples = None
	return avgSample

def plot(avgSample):
	pylab.plot(avgSample, label = "SimpleVirus")
	pylab.title("SimpleVirus simulation")
	pylab.xlabel("Time Steps")
	pylab.ylabel("Average Virus Population")
	pylab.legend(loc = "best")
	pylab.show()

# plot(simulationWithoutDrug(1, 10, 1.0, 0.0, 1))
# plot(simulationWithoutDrug(100, 200, 0.2, 0.8, 1))
# plot(simulationWithoutDrug(1, 90, 0.8, 0.1, 1))
plot(simulationWithoutDrug(100, 1000, 0.1, 0.05, 100))