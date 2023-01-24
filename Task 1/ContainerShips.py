# Container 1 -> 20feet long, weight 2tons and loads 20tons of freight
# Container 2 -> 40feet long, weight 4tons and loads 22tons of freight

# Ships -> L x W x H measured in bay in 20feet containers, typical L = 23, W = 22, H = 18


import random

class Container:
    def __init__(self, length, weight, freight, id):
        self.length = length
        self.weight = weight
        self.freight = freight
        self.id = id

    def setContainer(self, length, weight, freight):
        self.length = length
        self.weight = weight
        self.freight = freight

    def getContainer(self):
        return self

    def __str__(self):
        return str(self.id) + "\t" + str(self.length) + "\t" + str(self.weight) + "\t" + str(self.freight)


# print(Container(20, 2, 20, 1))


#code = id
def randomContainer():
    length = random.sample((20,40), 1)[0]
    if length > 0:
        if length <=20:
            weight = 2
            code = id(random.sample(range(1, 101), 1)[0])
            load = random.sample(range(0, 20), 1)[0]

        elif length <=40:
            weight = 4
            code = id(random.sample(range(1, 101), 1)[0])
            load = random.sample(range(0, 22), 1)[0]
    return Container(length, weight, load, code)

def randomContainers():
    containers = []
    for i in range(0, 100):
        containers.append(randomContainer())
    return set(containers)


def writeContainersToFile(containers):
    file = open("containers.txt","w")
    for container in containers:
        file.write(str(container) + "\n")


def readContainersFromFile():
    containers = []
    file = open("containers.txt","r")
    for line in file:
        line = line.split("\t")
        containers.append(Container(int(line[1]), int(line[2]), int(line[3]), int(line[0])))
    return containers

# (readContainersFromFile())

class Ship:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.containers = []
        #Ingen måte for å sjekke hvilken container som er i hvilken posisjon
        self.capacity = [length, width, height]
        

    def addContainer(self, container):
        if self.capacity[1] >= container.width and self.capacity[2] >= container.height and self.capacity[0] >= container.length:
            if self.capacity[1] >= container.width and self.capacity[0] >= container.length:
                self.containers.append(container)
                self.capacity[1] -= container.width
                self.capacity[0] -= container.length
            #Sjekke om det er plass til flere i høyden
            elif self.capacity[2] >= container.height:
                self.containers.append(container)
                self.capacity[0] += self.length - container.length
                self.capacity[1] += self.width - container.width
                self.capacity[2] -= container.height
        else:
            print("Container does not fit")

    def getContainers(self):
        return self.containers
    
    def removeContainer(self, container):
        if self.containers.__contains__(container):
            self.containers.remove(container)
        

    def findContainer(self, id):
        for container in self.containers:
            if self.container.id == id:
                return container
    
newShip = Ship(23, 22, 18)
newShip.addContainer(randomContainer())
print(newShip.getContainers())