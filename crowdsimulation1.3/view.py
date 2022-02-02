from click._compat import raw_input
from model import City
from model import Human
from model import Simulation
import matplotlib.pyplot as plt
import matplotlib.animation as ma
plt.style.use('fivethirtyeight')
#fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1,figsize=(30,10), gridspec_kw={'height_ratios': [5, 10]})

#locate the figure location
fig3 = plt.figure(constrained_layout=True)
gs = fig3.add_gridspec(2, 2)
ax1 = fig3.add_subplot(gs[0, :])
ax1.set_title('Crowd_Simulation')
ax2 = fig3.add_subplot(gs[1, 0])
ax2.set_title('Infection Vs. UnInfection')
ax3 = fig3.add_subplot(gs[1, 1])
ax3.set_title('People in "special" scope')

#set size

# set label names
ax1.set_xlabel("road")
ax1.set_ylabel("road")
ax2.set_xlabel("time")
ax2.set_ylabel("Number of people")
ax3.set_xlabel("time")
ax3.set_ylabel("people in scope")



# Main Menu In Terminal
runLoop = True
leftGroup = 30
rightGroup = 30
percentage0fInitialInfection = 0.1
infectionRate = 0.5
theRange = 3

menu_options = {
    1: 'Option 1  Quick Start Use default value',
    2: 'Option 2  Set values and Start',
    3: 'Option 3  See default value',
    4: 'Exit',
}
def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
    global runLoop
    runLoop = False


def option2():
    global leftGroup, rightGroup, percentage0fInitialInfection, infectionRate, theRange, runLoop
    print('Please Enter (?, ?, ?, ?, ?)')
    leftGroup = int(raw_input("Enter left group Number!\n"))
    rightGroup = int(raw_input("(%d, ?, ?, ?, ?)\nEnter right group Number!\n" %leftGroup))
    percentage0fInitialInfection = float(raw_input("(%d, %d, ?, ?, ?)\nEnter percentage of initial infection! (like '0.8')\n"%(leftGroup,rightGroup)))
    infectionRate =  float(raw_input("(%d, %d, %.2f, ?, ?)\nEnter infection rate! (like '0.5')\n"%(leftGroup, rightGroup, percentage0fInitialInfection)))
    theRange = int(raw_input("(%d, %d, %.2f, %2f, ?)\nset distance of scope which count! (like '3')\n"%(leftGroup, rightGroup, percentage0fInitialInfection, infectionRate)))
    runLoop = False



def option3():
    global leftGroup, rightGroup, percentage0fInitialInfection, infectionRate, theRange
    print('leftGroup: %d, rightGroup: %d, percentage0fInitialInfection: %.2f, infectionRate: %.2f, theRange: %d \n'
          %(leftGroup, rightGroup, percentage0fInitialInfection, infectionRate, theRange))

if __name__=='__main__':
    while(runLoop):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...\n')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            print('Thanks message before exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

# Main Menu Finish



sim=Simulation(leftGroup,rightGroup,percentage0fInitialInfection,infectionRate,theRange) # left group, right group, percentage of initial infection, infection rate%, set_distance of scope which count #meet

map=plt.imread("resources/yBmap.png")
ax1.imshow(map)
scInfected=ax1.scatter([],[],10, color='r')
scUnInfected=ax1.scatter([],[],10,color='g')
test=ax1.scatter([],[],10,color='blue')

test1=ax1.scatter([],[],10, color='r')
test2=ax1.scatter([],[],10,color='g')

# infect Vs uninfect
x_time = []
y_inf = []
y_uninf = []

# scope
y_scope = []

plt.tight_layout

iteration = 0
infect = 0
uninfect = 0


def update(number):
    global iteration
    global infect
    global uninfect
    sim.run()  # Run the simulation program
    iteration = sim.iteration
    infect = sim.infected
    uninfect = sim.uninfected
    print("Number of iterations：%d,Number of infections：%d，Number of healthy people：%d, count：%d, SD: %d, OD: %d, Scope: %d" % (iteration, infect, uninfect, sim.count, sim.passSD, sim.passOD, sim.scope))
    pos=sim.getHumanPosition()  #Calling People Location
    scInfected.set_offsets(pos["infected"])
    scUnInfected.set_offsets(pos["uninfected"])
    test.set_offsets(pos["special"])
    test1.set_offsets(pos["infectedR"])
    test2.set_offsets(pos["uninfectedR"])

    x_time.append(iteration)
    y_inf.append(infect)
    y_uninf.append(uninfect)

    y_scope.append(sim.scope)

    ax2.plot(x_time, y_inf, color='r')
    ax2.plot(x_time, y_uninf, color='g')

    ax3.plot(x_time, y_scope, color='blue')




anim = ma.FuncAnimation(plt.gcf(), update, interval=100)

plt.show()
