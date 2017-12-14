# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5

# For Python 3.6:
from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        # delta_y = speed * math.cos(math.radians(angle))
        # delta_x = speed * math.sin(math.radians(angle))
        rad = math.radians(angle) - 0.001  # Round floating point error
        delta_x = speed * math.cos(rad)
        delta_y = speed * math.sin(rad)
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        if width > 0 and height > 0:
            self.width = width
            self.height = height
            self.size = self.width * self.height
            self.tiles = dict()
            for i in range(width * height):
                self.tiles[i] = False
            self.cleanTileCount = 0
        else:
            raise RuntimeError("Width or height less than 0")

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        z = int(pos.getY()) * self.width + int(pos.getX())
        if self.tiles[z] is False:
            self.tiles[z] = True
            self.cleanTileCount += 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[n * self.width + m]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.size

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return self.cleanTileCount

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(
            random.uniform(0, self.width),
            random.uniform(0, self.height))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.getX() < 0.0 or pos.getY() < 0.0:
            return False
        if int(pos.getX()) >= self.width or int(pos.getY()) >= self.height:
            return False
        return True


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)
        self.degree = random.randint(0, 359)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.degree

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        if self.room.isPositionInRoom(position):
            self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        if direction >= 0 and direction < 360:
            self.degree = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.position.getNewPosition(self.degree, self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(newPos)
        else:
            degrees = list()
            w = float(self.room.width)
            h = float(self.room.height)
            yoverlap = 0
            xoverlap = 0
            dx = 0
            dy = 0
            sindy = 0
            cosdx = 0

            if self.position.getY() + self.speed >= h:
                dy = h - self.position.getY()
                sindy = int(math.degrees(math.asin(dy)))
                yoverlap = 1
            elif self.position.getY() - self.speed <= 0:
                dy = -self.position.getY()
                sindy = int(math.degrees(math.asin(dy)))
                yoverlap = -1

            if self.position.getX() + self.speed >= w:
                dx = w - self.position.getX()
                cosdx = int(math.degrees(math.acos(dx)))
                xoverlap = 1
            elif self.position.getX() - self.speed <= 0:
                dx = -self.position.getX()
                cosdx = int(math.degrees(math.acos(dx)))
                xoverlap = -1

            if yoverlap == 1:
                if xoverlap == 1:
                    degrees += [x for x in range(180 - sindy, 360 - cosdx)]
                elif xoverlap == -1:
                    degrees += [x for x in range(0, sindy)]
                    degrees += [x for x in range(180 + cosdx, 360)]
                elif xoverlap == 0:
                    degrees = [x for x in range(0, sindy)]
                    degrees += [x for x in range(180 - sindy, 360)]
            elif yoverlap == -1:
                if xoverlap == 1:
                    degrees = [x for x in range(cosdx, 270 + sindy)]
                elif xoverlap == -1:
                    degrees = [x for x in range(0, cosdx)]
                    degrees += [x for x in range(270 - sindy, 360)]
                elif xoverlap == 0:
                    degrees = [x for x in range(0, 270 + sindy)]
                    degrees += [x for x in range(270 - sindy, 360)]
            elif yoverlap == 0:
                if xoverlap == 1:
                    degrees += [x for x in range(cosdx, 360 - cosdx)]
                elif xoverlap == -1:
                    degrees = [x for x in range(0, cosdx)]
                    degrees += [x for x in range(180 + cosdx, 360)]

            if len(degrees) == 0:
                # in case, if compiler failed to identify floating point comparison
                degrees = [x for x in range(360)]

            od = self.degree
            d = random.choice(degrees)
            newPos = self.position.getNewPosition(d, self.speed)
            self.setRobotPosition(newPos)
            self.setRobotDirection(d)

            try:
                self.room.cleanTileAtPosition(newPos)
            except KeyError as err:
                print("Invalid key", err,
                    "|d", od, "|d1", d, "|dx", dx, "|dy", dy,
                    "|x", self.position.getX(), "|y", self.position.getY(),
                    "|x1", newPos.getX(), "|y1", newPos.getY())


# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)
# room = RectangularRoom(5, 5)
# stdRobot = StandardRobot(room, 1)
# stdRobot.setRobotPosition(Position(1.5, 2.5))
# stdRobot.setRobotDirection(90)
# for x in range(20):
#     stdRobot.updatePositionAndClean()

# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    # anim = ps2_visualize.RobotVisualization(num_robots, width, height)  # Start animation

    sumtime = 0
    for y in range(num_trials):
        room = RectangularRoom(width, height)
        rc = []
        for x in range(num_robots):
            rc.append(robot_type(room, speed))
        time = 0
        pc = 0.01
        while pc < min_coverage:
            pcl = []
            for r in rc:
                r.updatePositionAndClean()
                pcl.append(r.room.getNumCleanedTiles() / r.room.getNumTiles())
            time += 1
            pc = max(pcl)
            # anim.update(room, rc)  # Animate robot movement
        sumtime += time
        # anim.done()  # End of animation
    return sumtime / num_trials

# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))
# print(runSimulation(2, 1.0, 8, 8, 0.80, 30, StandardRobot))
# runSimulation(5, 1.0, 5, 5, 1.0, 30, StandardRobot)

# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        degrees = []
        w = float(self.room.width)
        h = float(self.room.height)
        yoverlap = 0
        xoverlap = 0
        dx = 0
        dy = 0
        sindy = 0
        cosdx = 0

        if self.position.getY() + self.speed >= h:
            dy = h - self.position.getY()
            sindy = int(math.degrees(math.asin(dy)))
            yoverlap = 1
        elif self.position.getY() - self.speed <= 0:
            dy = -self.position.getY()
            sindy = int(math.degrees(math.asin(dy)))
            yoverlap = -1

        if self.position.getX() + self.speed >= w:
            dx = w - self.position.getX()
            cosdx = int(math.degrees(math.acos(dx)))
            xoverlap = 1
        elif self.position.getX() - self.speed <= 0:
            dx = -self.position.getX()
            cosdx = int(math.degrees(math.acos(dx)))
            xoverlap = -1

        if yoverlap == 1:
            if xoverlap == 1:
                if self.degree > 180 - sindy and self.degree < 360 - cosdx:
                    degrees += [x for x in range(180 - sindy, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360 - cosdx)]
                else:
                    degrees += [x for x in range(180 - sindy, 360 - cosdx)]
            elif xoverlap == -1:
                if self.degree < sindy:
                    degrees += [x for x in range(0, self.degree)]
                    degrees += [x for x in range(self.degree + 1, sindy)]
                else:
                    degrees += [x for x in range(0, sindy)]
                if self.degree > 180 + cosdx:
                    degrees += [x for x in range(180 + cosdx, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360)]
                else:
                    degrees += [x for x in range(180 + cosdx, 360)]
            else:
                if self.degree < sindy:
                    degrees += [x for x in range(0, self.degree)]
                    degrees += [x for x in range(self.degree, sindy)]
                else:
                    degrees += [x for x in range(0, sindy)]
                if self.degree > 180 - sindy:
                    degrees += [x for x in range(180 - sindy, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360)]
                else:
                    degrees += [x for x in range(180 - sindy, 360)]
        elif yoverlap == -1:
            if xoverlap == 1:
                if self.degree > cosdx and self.degree < 270 + sindy:
                    degrees += [x for x in range(cosdx, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 270 + sindy)]
                else:
                    degrees += [x for x in range(cosdx, 270 + sindy)]
            elif xoverlap == -1:
                if self.degree < cosdx:
                    degrees += [x for x in range(0, self.degree)]
                    degrees += [x for x in range(self.degree + 1, cosdx)]
                else:
                    degrees += [x for x in range(0, cosdx)]
                if self.degree > 270 - sindy:
                    degrees += [x for x in range(270 - sindy, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360)]
                else:
                    degrees += [x for x in range(270 - sindy, 360)]
            else:
                if self.degree < 270 + sindy:
                    degrees += [x for x in range(0, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 270 + sindy)]
                else:
                    degrees += [x for x in range(0, 270 + sindy)]
                if self.degree > 270 - sindy:
                    degrees += [x for x in range(270 - sindy, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360)]
                else:
                    degrees += [x for x in range(270 - sindy, 360)]
        else:
            if xoverlap == 1:
                if self.degree > cosdx and self.degree < 360 - cosdx:
                    degrees += [x for x in range(cosdx, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360 - cosdx)]
                else:
                    degrees += [x for x in range(cosdx, 360 - cosdx)]
            elif xoverlap == -1:
                if self.degree < cosdx:
                    degrees += [x for x in range(0, self.degree)]
                    degrees += [x for x in range(self.degree + 1, cosdx)]
                else:
                    degrees += [x for x in range(0, cosdx)]
                if self.degree > 180 + cosdx:
                    degrees += [x for x in range(180 + cosdx, self.degree)]
                    degrees += [x for x in range(self.degree + 1, 360)]
                else:
                    degrees += [x for x in range(180 + cosdx, 360)]
            else:
                degrees += [x for x in range(0, self.degree)]
                degrees += [x for x in range(self.degree + 1, 360)]

        # print("xoverlap", xoverlap, "|yoverlap", yoverlap, "|degree",
        #     self.degree, "|cosdx", cosdx, "|sindy", sindy)
        d = random.choice(degrees)
        newPos = self.position.getNewPosition(d, self.speed)
        self.setRobotPosition(newPos)

        try:
            self.room.cleanTileAtPosition(newPos)
        except KeyError as err:
            print("Invalid key", err,
                "|d", self.degree, "|d1", d, "|dx", dx, "|dy", dy,
                "|x", self.position.getX(), "|y", self.position.getY(),
                "|x1", newPos.getX(), "|y1", newPos.getY())

        self.setRobotDirection(d)

# print(runSimulation(5, 1.0, 5, 5, 1.0, 30, RandomWalkRobot))
# runSimulation(5, 1.0, 5, 5, 1.0, 30, RandomWalkRobot)

def showPlot1(title, x_label, y_label):
    """
        Compare StandartRobot vs RandomWalkRobot in cleaning 80% of room
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


def showPlot2(title, x_label, y_label):
    """
        Compare StandartRobot vs RandomWalkRobot in cleaning 80% of varying
        room's width and height ratio
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# === Problem 6
# NOTE: If you are running the simulation, you will have to close it
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
# showPlot1("80 % cleaning", "Number of Robot", "Time Steps")

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
# showPlot2("80 % cleaning varying shape of room", "Aspect Ratio", "Time Steps")