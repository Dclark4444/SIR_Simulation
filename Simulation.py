import random
import turtle
import math
import numpy as np
import time

screen=turtle.getscreen()
screen.tracer(0)
turtle.up()
turtle.ht()
turtle.update()

SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
RECOVERED=(.5,.5,.5)
MOVE_DISTANCE = 1
testNumber = 2

#Mask Protection
maskSpreadChance = 0.5
maskProtectChance = 0.8

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
            if maskStatus == True:
                maskTemp1 = maskSpreadChance
            else:
                maskTemp1 = 1
            if other[4] == True:
                maskTemp2 = maskProtectChance
            else:
                maskTemp2 = 1
            if d<infectionRadius and d < random.randint(0, infectionRate*maskTemp1*maskTemp2):
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

def simulation(n=100,infectionRadius=10,infectionRate=10, m=0, averagePeriod = 240, show=False):
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

def averageData(dataSet):
    
    allS = []
    allI = []
    allR = []

    returnableData = []
    
    for w in dataSet:
        allS.append(w[0])
        allI.append(w[1])
        allR.append(w[2])

    allTypes = [allS, allI, allR]

    averagedData = []
    finalData = []

    for w in allTypes:
        averagedData = []

        #Average
        for x in range(0, len(w[0])):
            average = 0
            for y in w:
                average += y[x]
            averagedData.append(average/len(w))
        finalData.append(averagedData)
    returnableData.append(finalData)

    return returnableData

def saveData(data, title):
    with open(title, "w") as file:
        file.write(str(data))

def controlExperiment():
    #Sets up the variables to collect the averaged data later on
    dX = []
    dY = []
    dZ = []
    
    data = simulation()
    temp1 = data[0]
    temp1 = sum(temp1)/len(temp1)
    temp2 = data[1]
    temp2 = sum(temp2)/len(temp2)
    temp3 = data[2]
    temp3 = sum(temp3)/len(temp3)
    dX.append(temp1)
    dY.append(temp2)
    dZ.append(temp3)

    return (dX, dY, dZ)
    

#Defines the infectRadiusExperiment method that runs multiple simulations with an increasing infection radius and returns the averaged data collected as a tuple
def infectRadiusExperiment(lMin, lMax):
    #Sets up the variables to collect the averaged data later on
    dX = []
    dY = []
    dZ = []
 
    for x in range(lMax, lMin, -1):
        #print("Loading progress: " + str(lMax-x+1) + " out of " + str(lMax) + ".")
        data = simulation(infectionRadius=x)
        temp1 = data[0]
        temp1 = sum(temp1)/len(temp1)
        temp2 = data[1]
        temp2 = sum(temp2)/len(temp2)
        temp3 = data[2]
        temp3 = sum(temp3)/len(temp3)
        dX.append(temp1)
        dY.append(temp2)
        dZ.append(temp3)

    return (dX, dY, dZ)

#Defines the infectChanceExperiment method that runs multiple simulations with an increasing infection chance and returns the averaged data collected as a tuple
def infectChanceExperiment(lMin, lMax):
    #Sets up the variables to collect the averaged data later on
    dX = []
    dY = []
    dZ = []
 
    for x in range(lMax, lMin, -1):
        #print("Loading progress: " + str(lMax-x+1) + " out of " + str(lMax) + ".")
        data = simulation(infectionRate=x)
        temp1 = data[0]
        temp1 = sum(temp1)/len(temp1)
        temp2 = data[1]
        temp2 = sum(temp2)/len(temp2)
        temp3 = data[2]
        temp3 = sum(temp3)/len(temp3)
        dX.append(temp1)
        dY.append(temp2)
        dZ.append(temp3)

    return (dX, dY, dZ)

#Defines the infectChanceExperiment method that runs multiple simulations with an increasing infection chance and returns the averaged data collected as a tuple
def infectPeriodExperiment(lMin, lMax, stepC):
    #Sets up the variables to collect the averaged data later on
    dX = []
    dY = []
    dZ = []
 
    for x in range(lMax, lMin, -stepC):
        #print("Loading progress: " + str(lMax-x) + " out of " + str(lMax) + ".")
        data = simulation(averagePeriod=x)
        temp1 = data[0]
        temp1 = sum(temp1)/len(temp1)
        temp2 = data[1]
        temp2 = sum(temp2)/len(temp2)
        temp3 = data[2]
        temp3 = sum(temp3)/len(temp3)
        dX.append(temp1)
        dY.append(temp2)
        dZ.append(temp3)

    return (dX, dY, dZ)

#Defines the maskExperiment method that runs multiple simulations with an increasing number of masks being used each simulation and returns the averaged data collected as a tuple
def maskExperiment(mMin, mMax, stepC):
    #Sets up the variables to collect the averaged data later on
    dX = []
    dY = []
    dZ = []
 
    for x in range(mMin, mMax, stepC):
        #print("Loading progress: " + str(x) + " out of " + str(mMax-1) + ".")
        data = simulation(m=x)
        temp1 = data[0]
        temp1 = sum(temp1)/len(temp1)
        temp2 = data[1]
        temp2 = sum(temp2)/len(temp2)
        temp3 = data[2]
        temp3 = sum(temp3)/len(temp3)
        dX.append(temp1)
        dY.append(temp2)
        dZ.append(temp3)

    return (dX, dY, dZ)

        
#Defines the method that just runs the experiments created above
def experiments():

    #Collects a control simulation and collects the data. Then finally makes a graph of it
    controlData = []
    infectRadiusData= []
    infectChanceData = []
    infectPeriodData = []
    maskData = []

    for x in range(0, testNumber):
        controlData.append(controlExperiment())
        infectRadiusData.append(infectRadiusExperiment(0, 10))
        infectChanceData.append(infectChanceExperiment(0, 10))
        infectPeriodData.append(infectPeriodExperiment(59, 80, 10)) #(59, 240, 10)
        maskData.append(maskExperiment(0, 4, 2)) #(0, 101, 2)

    print(controlData)

    controlData = averageData(controlData)
    infectRadiusData= averageData(infectRadiusData)
    infectChanceData = averageData(infectChanceData)
    infectPeriodData = averageData(infectPeriodData)
    maskData = averageData(maskData)

    saveData(controlData, "Control_Data_Experiment.txt")
    saveData(infectRadiusData, "Infect_Radius_Experiment_Data.txt")
    saveData(infectChanceData, "Infect_Chance_Experiment_Data.txt")
    saveData(infectPeriodData, "Infect_Period_Experiment_Data.txt")
    saveData(maskData, "Mask_Experiment_Data.txt")

experiments()

#Begins the main loop for turtles so that they can method correctly 
turtle.mainloop()



