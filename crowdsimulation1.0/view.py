from model import City
from model import Human
from model import Simulation
import matplotlib.pyplot as plt
import matplotlib.animation as ma
sim=Simulation(200,0.05,0.2) #Total number of people, percentage of initial infection, % infection rate
map=plt.imread("resources/white2.png")
plt.imshow(map)
scInfected=plt.scatter([],[],10, color='r')
scUnInfected=plt.scatter([],[],10,color='g')


def update(number):
    sim.run()       #Run the simulation program
    print("Number of iterations：%d,Number of infections：%d，Number of healthy people：%d"%(sim.iteration,sim.infected,sim.uninfected))
    pos=sim.getHumanPosition()  #Calling People Location
    scInfected.set_offsets(pos["infected"])
    scUnInfected.set_offsets(pos["uninfected"])

anim = ma.FuncAnimation(plt.gcf(), update, interval=1)

plt.show()