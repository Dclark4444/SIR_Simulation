import matplotlib.pyplot as plt
import numpy as np
import ast

SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
RECOVERED=(.5,.5,.5)

#Defines the makeGraph method that intakes data as a tuple and an instance to produce a graph based off that data
def makeGraph(data, instance, title, xLabel):
    x=range(len(data[0]))
    TEMP = plt.figure(instance)
    plt.stackplot(x, data, labels=['Susceptible','Infected','Recovered'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED])
    plt.legend(loc='upper left')
    plt.xlabel(xLabel)
    plt.ylabel('Population')
    plt.title(title)
    plt.show(block=False)

listOfData = []
finalListOfData = []
listOfFileNames = ['Infect_Chance_Experiment_Data.txt', 'Infect_Period_Experiment_Data.txt', 'Infect_Radius_Experiment_Data.txt', 'Mask_Experiment_Data.txt']
listOfXLabels = ['Infect Chance', 'Infect Period', 'Infect Radius', 'Masks Used']
for x in listOfFileNames:
    with open(x, 'r') as FILE:
        listOfData.append(FILE.read())

for x in listOfData:
    finalListOfData.append(ast.literal_eval(x))

for x in range(0, len(finalListOfData)):
    makeGraph(finalListOfData[x][0], x, listOfFileNames[x][:-4].replace('_', ' '), listOfXLabels[x])


