import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up,
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    pRep = 1 - (CURRENTRABBITPOP / MAXRABBITPOP)
    if random.random() <= pRep and CURRENTRABBITPOP < MAXRABBITPOP:
        CURRENTRABBITPOP += 1

def foxGrowth():
    """
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    pEat = CURRENTRABBITPOP / MAXRABBITPOP
    p = random.random()
    if CURRENTRABBITPOP > 10 and p <= pEat:
        CURRENTRABBITPOP -= 1
        if p <= 1/3:
            CURRENTFOXPOP += 1
    else:
        if CURRENTFOXPOP > 10:
            if p <= 1/10:
                CURRENTFOXPOP -= 1

def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbit_populations = []
    fox_populations = []
    for step in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)
    return rabbit_populations, fox_populations


# rabbit_populations, fox_populations = runSimulation(10000)

# pylab.figure()
# pylab.plot(rabbit_populations, 'ob', label = "Rabbit Population")
# pylab.plot(fox_populations, 'or', label = "Fox Population")
# crabbit = pylab.polyfit(range(len(rabbit_populations)), rabbit_populations, 2)
# fitRabbit = pylab.polyval(crabbit, range(len(rabbit_populations)))
# pylab.plot(fitRabbit, '-g', label='Fit Rabbit')
# cfox = pylab.polyfit(range(len(fox_populations)), fox_populations, 2)
# fitFox = pylab.polyval(cfox, range(len(fox_populations)))
# pylab.plot(fitFox, '-y', label='Fit Fox')
# pylab.title("Rabbit And Fox Populations")
# pylab.xlabel("Time Steps")
# pylab.ylabel("Populations")
# pylab.legend()

# pylab.show()

# Test
random.seed(0)
print("Test 1")
print("Calling rabbitGrowth with MAXRABBITPOP = 1000, CURRENTRABBITPOP = 500 should increase the population.")
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
c = CURRENTRABBITPOP
rabbitGrowth()
print(CURRENTRABBITPOP)
print("Population has increased? {}".format(CURRENTRABBITPOP>c))
c = CURRENTRABBITPOP
rabbitGrowth()
print(CURRENTRABBITPOP)
print("Population has increased? {}".format(CURRENTRABBITPOP>c))

random.seed(0)
print()
print("Test 2")
print("Calling rabbitGrowth with MAXRABBITPOP = 1000, CURRENTRABBITPOP = 1000 should NOT increase the population.")
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 1000
c = CURRENTRABBITPOP
rabbitGrowth()
print("Population has increased? {}".format(CURRENTRABBITPOP>c))
c = CURRENTRABBITPOP
rabbitGrowth()
print("Population has increased? {}".format(CURRENTRABBITPOP>c))

random.seed(0)
print()
print("Test 3")
print("Calling foxGrowth with CURRENTRABBITPOP = 1000, MAXRABBITPOP = 1000, CURRENTFOXPOP = 50 should increase the population.")
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 1000
CURRENTFOXPOP = 50
c = CURRENTFOXPOP
foxGrowth()
print(CURRENTFOXPOP)
print("Population has increased? {}".format(CURRENTFOXPOP>c))
c = CURRENTFOXPOP
foxGrowth()
print(CURRENTFOXPOP)
print("Population has increased? {}".format(CURRENTFOXPOP>c))

random.seed(0)
print()
print("Test 4")
print("Calling foxGrowth with CURRENTRABBITPOP = 1, MAXRABBITPOP = 1000, CURRENTFOXPOP = 1 should NOT increase the population.")
CURRENTRABBITPOP = 1
MAXRABBITPOP = 1000
CURRENTFOXPOP = 1
print("Calling foxGrowth() 20 times. The fox population should NOT grow.")
c = CURRENTFOXPOP
for i in range(20):
    foxGrowth()
print("Population has increased? {}".format(c>CURRENTFOXPOP))

print()
print("Test 5")
print("Test the simulation")
runSimulation(20)
print("results = runSimulation(20)")
print(True)

random.seed(0)
print()
print("Test 6")
print("Test the simulation with CURRENTRABBITPOP = 10, CURRENTFOXPOP = 20, MAXRABBITPOP = 100")
CURRENTRABBITPOP = 10
CURRENTFOXPOP = 20
MAXRABBITPOP = 100
results = runSimulation(100)
print("results = runSimulation(100)")
rabbitAbove10 = True
rabbitBelow100 = True
for rb in results[0]:
    if rabbitAbove10 is not True and rabbitBelow100 is not True:
        break
    if rb < 10 and rabbitAbove10:
        rabbitAbove10 = False
    if rb > 100 and rabbitBelow100:
        rabbitBelow100 = False
print("Testing that the number of rabbits never falls below 10: {}".format(rabbitAbove10))
print("or goes above 100: {}".format(rabbitBelow100))

print()
print("Test 7")
print("Test the simulation with CURRENTRABBITPOP = 10, CURRENTFOXPOP = 20, MAXRABBITPOP = 100")
print("results = runSimulation(100)")
foxAbove10 = True
for fx in results[1]:
    if fx < 10:
        foxAbove10 = True
        break
print("Testing that the number of foxes never falls below 10: {}".format(foxAbove10))