import matplotlib.pyplot as plt
import numpy as np

SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
RECOVERED=(.5,.5,.5)

#Defines the makeGraph method that intakes data as a tuple and an instance to produce a graph based off that data
def makeGraph(data, instance, title):
    x=range(len(data[0]))
    TEMP = plt.figure(instance)
    plt.stackplot(x, data, labels=['Susceptible','Infected','Recovered'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED])
    plt.legend(loc='upper left')
    plt.xlabel('step count')
    plt.ylabel('population')
    plt.title(title)
    plt.show(block=False)

listOfData = []
tempList = []
finalListOfData = []
listOfFileNames = ["Control_Data_Experiment.txt", "Infect_Chance_Experiment_Data.txt", "Infect_Period_Experiment_Data.txt", "Infect_Radius_Experiment_Data.txt", "Mask_Experiment_Data.txt"]

for x in listOfFileNames:
    with open(x, "r") as FILE:
        listOfData.append(FILE.read())
        
for x in listOfData:
    tempList.append(x.strip("][").split(", "))
    
for x in tempList:
    temp = []
    for y in x:
        temp.append(float(y.strip("][")))
    finalListOfData.append(temp)

print(finalListOfData)

for x in range(0, len(finalListOfData)):
    makeGraph(finalListOfData[x], x, listOfFileNames[x][:-4])


