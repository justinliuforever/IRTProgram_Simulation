import random
import numpy as np
import time




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
                    self.map[row][col] = line[col]  # Input each point on the txt (city.map)）

    def canMove(self, x, y):  # See if the place can go, such as a wall("1") or something, and not beyond the border
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            return self.map[y][x] == '0';  # return value if can move
        else:
            return False;


class Human():
    ##x,y_every person's location ##city_Used to determine if the place can be walked
    def __init__(self, x, y, city, infected=False):  # Initialization
        super().__init__()
        self.x = x
        self.y = y
        self.city = city
        self.infected = infected
        ##self.id = 0.0
        self.meet = False

    def move(self):  # Control the direction of human move to left
        r = random.randint(0, 4)
        s = random.randint(1, 1)
        if r == 0:
            if self.city.canMove(self.x - 1, self.y):
                self.x -= s
        elif r == 1 or r == 2 or r == 3 or r == 4:  # The probability of people going to the left is 4/6
            if self.city.canMove(self.x - 1, self.y):
                self.x -= s
        elif r == 5:
            if self.city.canMove(self.x, self.y + 1):
                self.y += 1
        else:
            if self.city.canMove(self.x, self.y - 1):
                self.y -= 1

    ##test2
    def moveRight(self):  # Control the direction of human move
        r = random.randint(0, 4)
        s = random.randint(1, 1)
        if r == 0:
            if self.city.canMove(self.x + 1, self.y):
                self.x += s
        elif r == 1 or r == 2 or r == 3 or r == 4:  # The probability of people going to the left is 4/6
            if self.city.canMove(self.x + 1, self.y):
                self.x += s
        elif r == 5:
            if self.city.canMove(self.x, self.y + 1):
                self.y += 1
        else:
            if self.city.canMove(self.x, self.y - 1):
                self.y -= 1

    def specialV(self):  #consistent to left
        r = random.randint(0, 4)
        if r == 0:
            if self.city.canMove(self.x - 2, self.y):
                self.x -= 2
        elif r == 1 or r == 2 or r == 3 or r == 4:  # The probability of people going to the left is 4/6
            if self.city.canMove(self.x - 2, self.y):
                self.x -= 2
        elif r == 5:
            if self.city.canMove(self.x, self.y + 1):
                self.y += 1
        else:
            if self.city.canMove(self.x, self.y - 1):
                self.y -= 1


##

class Simulation:
    def __init__(self, humanSize, humanSizeR, iRatio, p, dis):
        super().__init__()
        self.city = City("resources/yBmap.txt")  # Load map_via the City() class written above
        self.p = p
        self.humans = []

        # TEST
        self.special = []
        self.humansRight = []
        self.count = 0    # how many people that special person meet
        self.passSD = 0   # how many people the special person pass by in same direction
        self.passOD = 0   # how many people the special person pass by in different direction
        self.scope = 0    # count how many people "special near by"
        self.dis = dis    # the range which we count meet people

        # Initial Each person, randomly placed anywhere
        for i in range(0, humanSize):
            #self.id = time.time()
            while True:
                x = random.randint(0, self.city.w - 1)
                y = random.randint(0, self.city.h - 1)
                if self.city.map[y][x] == '0':
                    break
            self.humans.append(Human(x, y, self.city))
        # Initial Special persons
        for i in range(0, 1):
            while True:
                #x = random.randint(self.city.w - 10, self.city.w - 1)  # '-2' minus the contained boundary
                #y = random.randint( self.city.h - 10, self.city.h - 1)
                x = 447
                y = 3
                #print(x)
                #print(y)

                if self.city.map[y][x] == '0':  # Determine if the point is a wall or a boundary (only "0" is allowed to go)
                    break
            self.special.append(Human(x, y, self.city))  # special.infected(default)

        # Initial people toward right
        for i in range(0, humanSizeR):
            while True:
                x = random.randint(0, self.city.w - 1)
                y = random.randint(0, self.city.h - 1)
                if self.city.map[y][x] == '0':
                    break
            self.humansRight.append(Human(x, y, self.city))
        # FINISH


        # Initial Infection people #
        # Initialize ———— initial how many infected people at the beginning
        for i in range(0, int(humanSize * iRatio)):
            self.humans[i].infected = True

        # Initialize ———— initial how many infected peopleRight at the beginning
        for i in range(0,int(humanSizeR * iRatio)):
            self.humansRight[i].infected = True
        self.infected = int(humanSize * iRatio) + int(humanSizeR * iRatio)  # Start recording information
        self.uninfected = humanSize + humanSizeR - self.infected
        self.iteration = 0

    ##TEST
    # self.count = 0

    def run(self):
        global count
        global passSD
        global passOD
        global scope
        global dis
        self.scope = 0
        self.iteration += 1
        # move toward left
        for human in self.humans:
            if human.x < self.city.w - 1 and human.x > 0:
                human.move()  # All human  move once
            else:
                human.x = self.city.w - 2  #move to the right side
                #human.id = time.time()
                human.meet = False
        # TEST
        for spe in self.special:  # run as above
            if spe.x < self.city.w - 1 and spe.x > 0:
                spe.specialV()  # special move once
            else:
                spe.x = self.city.w - 2

        for humanR in self.humansRight:  # run as above
            if humanR.x < self.city.w - 1 and humanR.x > 0:
                humanR.moveRight()  # All humanR  move once (Right)
            else:
                humanR.x = 1
                #human.id = time.time()
                human.meet = False
        ##

        # When an uninfected person comes into contact with an infected person, the person
        # is infected ## but when the person reaches the border between the two sides (after this intersection),
        # it is not infected ( simulated person has already passed this place and is no longer recorded)

        # humans infect humans
        for human in self.humans:
            for other in self.humans:
                if human != other and human.x == other.x and human.y == other.y and human.x < self.city.w - 1 and human.x > 0:
                    if human.infected and (not other.infected):
                        if random.random() < self.p:
                            other.infected = True

        # humansRight infect humansRight
        for human in self.humansRight:
            for other in self.humansRight:
                if human != other and human.x == other.x and human.y == other.y and human.x < self.city.w - 1 and human.x > 0:
                    if human.infected and (not other.infected):
                        if random.random() < self.p:
                            other.infected = True

        # humans infect humansRight
        for human in self.humans:
            for other in self.humansRight:
                if human != other and human.x == other.x and human.y == other.y and human.x < self.city.w - 1 and human.x > 0:
                    if human.infected and (not other.infected):
                        if random.random() < self.p:
                            other.infected = True


        # test
        ## count how many people the "special" people meet
        for human in self.humans:
            for spe in self.special:
                if human != spe and abs(human.x-spe.x)<3 and abs(human.y-spe.y)<3 and spe.x < self.city.w - 1 and spe.x > 0 and human.meet == False:
                    self.count = self.count + 1  # meet people
                    self.passSD = self.passSD + 1
                    human.meet = True

        for human in self.humansRight:
            for spe in self.special:
                if human != spe and abs(human.x-spe.x)<3 and abs(human.y-spe.y)<3 and spe.x < self.city.w - 1 and spe.x > 0 and human.meet == False:
                    self.count = self.count + 1  # meet people
                    self.passOD = self.passOD + 1
                    human.meet = True
        ##
        ##calclate scope
        for human in self.humans:
            for spe in self.special:
                if human != spe and (abs(human.x-spe.x)<self.dis) and (abs(human.y-spe.y)<self.dis):
                    self.scope = self.scope + 1  # plus one more people

        for human in self.humansRight:
            for spe in self.special:
                if human != spe and (abs(human.x-spe.x)<self.dis) and (abs(human.y-spe.y)<self.dis):
                    self.scope = self.scope + 1  # plus one more people


        self.infected = 0
        for human in self.humans:
            if human.infected:
                self.infected += 1
 ##
        for human in self.humansRight:
            if human.infected:
                self.infected += 1

        self.uninfected = len(self.humans) + len(self.humansRight) - self.infected

    def getHumanPosition(self):
        infectedPos = []
        unInfectedPos = []

        infectedPosR = []
        unInfectedPosR = []
        ##TEST
        specialPos = []
        for i in range(len(self.special)):
            specialPos.append((self.special[i].x * self.city.cell + self.city.cell // 2,
                               self.special[i].y * self.city.cell + self.city.cell // 2))
        ##
        for i in range(len(self.humans)):  # Make two lists with the coordinates of the infected and the infected
            if self.humans[i].infected:  # The latter piece "*self.city.cell+self.city.cell//2" is to fit the image
                # and make the point appear in the middle of each cell on the graph when the program runs
                infectedPos.append((self.humans[i].x * self.city.cell + self.city.cell // 2,
                                    self.humans[i].y * self.city.cell + self.city.cell // 2))
            else:
                unInfectedPos.append((self.humans[i].x * self.city.cell + self.city.cell // 2,
                                      self.humans[i].y * self.city.cell + self.city.cell // 2))

        for i in range(len(self.humansRight)):  # Make two lists with the coordinates of the infected and the infected
            if self.humansRight[i].infected:  # The latter piece "*self.city.cell+self.city.cell//2" is to fit the image
                # and make the point appear in the middle of each cell on the graph when the program runs
                infectedPosR.append((self.humansRight[i].x * self.city.cell + self.city.cell // 2,
                                    self.humansRight[i].y * self.city.cell + self.city.cell // 2))
            else:
                unInfectedPosR.append((self.humansRight[i].x * self.city.cell + self.city.cell // 2,
                                      self.humansRight[i].y * self.city.cell + self.city.cell // 2))

        return {"infected": np.array(infectedPos), "uninfected": np.array(unInfectedPos),
                "infectedR": np.array(infectedPosR), "uninfectedR": np.array(unInfectedPosR),
                "special": np.array(specialPos)}

# sim=Simulation(500,0.1,0.1)
# for i in range(1000):
#    sim.run()
#
