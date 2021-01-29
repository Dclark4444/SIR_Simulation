import random
import turtle
import math
import time
import matplotlib.pyplot as plt

screen=turtle.getscreen()
screen.tracer(0)
turtle.up()
turtle.ht()
turtle.update()

SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
RECOVERED=(.5,.5,.5)
MOVE_DISTANCE=1

#Mask Protection
maskSpreadChance = 0.5
maskProtectChance = 0.5

def getPopulation(n, m):
    masksLeft = m
    population=[]
    for i in range(n):
        x=random.uniform(-200,200)
        y=random.uniform(-200,200)
        direction=random.uniform(0,360)
        status=SUSCEPTIBLE
        if masksLeft > 0:
            maskStatus = True
            masksLeft =- 1
        else:
            maskStatus = False
            
        population.append([x,y,status,direction, maskStatus, ""])
    return population

def infectPopulation(population,n=1):
    while n:
        person=random.choice(population)
        if person[2]==SUSCEPTIBLE:
            person[2]=INFECTED
            n-=1

def display(population):
    turtle.clear()
    turtle.goto(220,220)
    turtle.down()
    turtle.seth(180)
    for i in range(4):
        turtle.forward(440)
        turtle.left(90)
    turtle.up()
    turtle.shapesize(2,2)
    for x,y,status,direction,masks,infectionPeriod in population:
        turtle.goto(x,y)
        turtle.seth(direction)
        turtle.fillcolor(status)
        turtle.stamp()
    turtle.update()

def step(population,infectionRadius,infectionRate, averagePeriod):
    for person in population:
        x,y,status,direction, maskStatus, infectionPeriod = person
        x+=MOVE_DISTANCE*math.cos(direction/180*math.pi)
        y+=MOVE_DISTANCE*math.sin(direction/180*math.pi)
        direction+=random.uniform(-5,5)
        if x<-200 or x>200:
            direction=180-direction
        if y>200 or y<-200:
            direction=-direction
        person[0]=x
        person[1]=y
        person[3]=direction
        if status==SUSCEPTIBLE:
            expose(person,population,infectionRadius,infectionRate)
        elif status==INFECTED:
            if infectionPeriod == "":
                assignRecoveryPeriod(person, averagePeriod)
            else:
                person[5] -= 1
                if person[5] <= 0:
                    person[2] = RECOVERED
            
def expose(person,population,infectionRadius,infectionRate):
    x,y,status,direction, maskStatus, infectionPeriod = person
    for other in population:
        if other[2]==INFECTED:
            i,j,*_=other
            d=math.hypot(x-i,y-j)
            if d<infectionRadius and d < random.randint(0, infectionRadius):
                person[2]=INFECTED
                break

def assignRecoveryPeriod(person, averagePeriod):
    person[5] = random.gauss(averagePeriod, 40)

def census(population):
    s=i=r=0
    for _,_,status,_, masks, infectionPeriod in population:
        s+=status==SUSCEPTIBLE
        i+=status==INFECTED
        r+=status==RECOVERED
    return s,i,r

def simulation(n=100,infectionRadius=10,infectionRate=.1, m=0, averagePeriod = 240, show=True):
    population=getPopulation(n, m)
    infectPopulation(population)
    S=[]
    I=[]
    R=[]
    while not I or I[-1]>0:
        step(population,infectionRadius,infectionRate, averagePeriod)
        s,i,r=census(population)
        S.append(s)
        I.append(i)
        R.append(r)
        if show:
            display(population)
    return S,I,R

#Defines the makeGraph function that intakes data as a tuple and an instance to produce a graph based off that data
def makeGraph(data, instance, title):
    x=range(len(data[0]))
    TEMP = plt.figure(instance)
    plt.stackplot(x,data, labels=['Susceptible','Infected','Recovered'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED])
    plt.legend(loc='upper left')
    plt.xlabel('step count')
    plt.ylabel('population')
    plt.title(title)
    plt.show(block=False)

#Defines the infectRadiusExperiment function that runs multiple simulations with an increasing infection radius and returns the averaged data collected as a tuple
def infectRadiusExperiment(Lmin, Lmax):
    #Sets up the variables to collect the averaged data later on
    infectRadiusX = []
    infectRadiusY = []
    infectRadiusZ = []
 
    for x in range(Lmin, Lmax, 1):
        print("Loading progress: " + str(x) + " out of " + str(Lmax-1) + ".")
        data = simulation(show=False, infectionRadius=x)
        temp1 = data[0]
        temp1 = sum(temp1)/len(temp1)
        temp2 = data[1]
        temp2 = sum(temp2)/len(temp2)
        temp3 = data[2]
        temp3 = sum(temp3)/len(temp3)
        infectRadiusX.append(temp1)
        infectRadiusY.append(temp2)
        infectRadiusZ.append(temp3)

    return (infectRadiusX, infectRadiusY, infectRadiusZ)

#Defiens the function that just runs the experiments created above
def experiments():

    #Collects a control simulation and collects the data. Then finally makes a graph of it
    controlData=simulation(show=True)
    makeGraph(controlData, 1, "Control Experiment")

experiments()

#Begins the main loop for turtles so that they can function correctly 
turtle.mainloop()



