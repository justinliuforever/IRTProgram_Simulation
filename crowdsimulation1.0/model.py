import random
import numpy as np


class City():
    def __init__(self, fileName):  ###Load Map###
        super().__init__()
        with open(fileName, "r") as f:
            self.w = int(f.readline())
            self.h = int(f.readline())
            self.cell = int(f.readline())  # Size of each cell
            self.map = [['0' for col in range(0, self.w)] for row in
                        range(0, self.h)]  # initialize the array ,creat 2d array, Default all equal to '0'
            for row in range(0, self.h):  # start reading the map
                line = f.readline()
                for col in range(0, self.w):
                    self.map[row][col] = line[col]  # Input each point on the txt (city.map)

    def canMove(self, x, y):  # See if the place can go, such as a wall("1") or something, and not beyond the border
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            return self.map[y][x] == '0'  # return tru if can move
        else:
            return False


class Human():
    ##x,y_every person's location ##city_Used to determine if the place can be walked
    def __init__(self, x, y, city, infected=False):  # Initialization
        super().__init__()
        self.x = x
        self.y = y
        self.city = city
        self.infected = infected

    def move(self):  # Control the direction of human move
        r = random.randint(0, 6)
        if r == 0:
            if self.city.canMove(self.x + 1, self.y):
                self.x += 1
        elif r == 1 or r == 2 or r == 3 or r == 4:  # The probability of people going to the left is 4/6
            if self.city.canMove(self.x - 1, self.y):
                self.x -= 1
        elif r == 5:
            if self.city.canMove(self.x, self.y + 1):
                self.y += 1
        else:
            if self.city.canMove(self.x, self.y - 1):
                self.y -= 1


class Simulation:
    def __init__(self, humanSize, iRatio, p):
        super().__init__()
        self.city = City("resources/map.txt")  # Load map_via the City() class written above
        self.p = p
        self.humans = []

        for i in range(0, humanSize):  # initial Each person, randomly placed anywhere
            while True:
                x = random.randint(0, self.city.w - 1)  # '-1' minus the contained boundary
                y = random.randint(0, self.city.h - 1)
                if self.city.map[y][
                    x] == '0':  # Determine if the point is a wall or a boundary (only "0" is allowed to go)
                    break
            self.humans.append(Human(x, y, self.city))  # when the place is walkable (x,y,map information)，Record the location of the person

        for i in range(0, int(humanSize * iRatio)):  # Initialize ———— initial how many infected people at the beginning
            self.humans[i].infected = True
        self.infected = int(humanSize * iRatio)  # Start recording information
        self.uninfected = humanSize - self.infected
        self.iteration = 0

    def run(self):
        self.iteration += 1
        for human in self.humans:  # 开始循环human这个array
            if human.x < self.city.w - 1 and human.x > 0:
                human.move()  # All human  move once

        # When an uninfected person comes into contact with an infected person, the person
        # is infected ## but when the person reaches the border between the two sides (after this intersection),
        # it is not infected ( simulated person has already passed this place and is no longer recorded)
        for human in self.humans:
            for other in self.humans:
                if human != other and human.x == other.x and human.y == other.y and human.x < self.city.w - 1 and human.x > 0:
                    if human.infected and (not other.infected):
                        if random.random() < self.p:
                            other.infected = True
        self.infected = 0
        for human in self.humans:
            if human.infected:
                self.infected += 1
        self.uninfected = len(self.humans) - self.infected

    def getHumanPosition(self):
        infectedPos = []
        unInfectedPos = []
        for i in range(len(self.humans)):  # Make two lists with the coordinates of the infected and the infected
            if self.humans[i].infected:  # The latter piece "*self.city.cell+self.city.cell//2" is to fit the image
                                        # and make the point appear in the middle of each cell on the graph when the program runs
                infectedPos.append((self.humans[i].x * self.city.cell + self.city.cell // 2,
                                    self.humans[i].y * self.city.cell + self.city.cell // 2))
            else:
                unInfectedPos.append((self.humans[i].x * self.city.cell + self.city.cell // 2,
                                      self.humans[i].y * self.city.cell + self.city.cell // 2))
        return {"infected": np.array(infectedPos), "uninfected": np.array(unInfectedPos)}

# sim=Simulation(500,0.1,0.1)
# for i in range(100):
#     sim.run()
#     print("Number of iterations：%d,Number of infections：%d，Number of healthy people：%d"%(sim.iteration,sim.infected,sim.uninfected))
