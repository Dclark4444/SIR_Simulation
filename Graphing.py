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

#makeGraph(controlData, 1, "Control Experiment")
#makeGraph(infectRadiusData, 2, "Infection Radius Experiment")
#makeGraph(maskData, 3, "Mask Experiment")

