import matplotlib.pyplot as plt
import numpy as np

SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
RECOVERED=(.5,.5,.5)

#Defines the makeGraph method that intakes data as a tuple and an instance to produce a graph based off that data
def makeGraph(data, instance, title):
    x=range(len(data[0]))
    TEMP = plt.figure(instance)
    plt.stackplot(x,data, labels=['Susceptible','Infected','Recovered'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED])
    plt.legend(loc='upper left')
    plt.xlabel('step count')
    plt.ylabel('population')
    plt.title(title)
    plt.show(block=False)
    
makeGraph(np.asarray(controlData), 1, "Control Experiment")
#makeGraph(np.asarray(infectRadiusData), 2, "Infection Radius Experiment")
#makeGraph(np.asarry(maskData), 3, "Mask Experiment")

