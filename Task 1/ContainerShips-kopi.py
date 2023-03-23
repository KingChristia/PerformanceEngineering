# Container 1 -> 20feet long, weight 2tons and loads 20tons of freight
# Container 2 -> 40feet long, weight 4tons and loads 22tons of freight

# Ships -> L x W x H measured in bay in 20feet containers, typical L = 23, W = 22, H = 18


import timeit
import random
import datetime


class Container:
    #Container Constructor
    def __init__(self, length, weight, freight, id):
        self.length = length
        self.weight = weight
        self.freight = freight
        self.id = id
        self.big = True if length == 40 else False   # Boolean
        self.position = [0, 0, 0]

    def setContainer(self, length, weight, freight):
        self.length = length
        self.weight = weight
        self.freight = freight

    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position

    def getLength(self):
        return self.length

    def getId(self):
        return self.id

    def getWeight(self) -> int:
        return int(self.weight)

    def getFreight(self) -> int:
        return int(self.freight)

    def setFreight(self, newFreight):
        self.freight = newFreight

    def getContainer(self):
        return self

    def isBigContainer(self):
        return self.big

    def getTotalWeight(self) -> int:
        return self.getWeight() + self.getFreight()

    def __str__(self):
        return str(self.id) + "\t" + str(self.length) + "\t" + str(self.weight) + "\t" + str(self.freight)




# code = id
def randomContainer() -> (Container):
    #Random length of container, 20 or 40
    length = random.sample((20, 40), 1)[0]
    if length > 0:
        if length <= 20:
            weight = 2
            #Uses python builtin id function to generate a unique id with datetime now as seed, for a unique id
            code = id(datetime.datetime.now())
            load = random.sample(range(0, 20), 1)[0]
        elif length <= 40:
            weight = 4
            code = id(datetime.datetime.now())
            load = random.sample(range(0, 22), 1)[0]
    return Container(length, weight, load, code)


def randomContainers():
    containers = []
    # 6600 containers in this method for typical ship in this task.
    # Can be changed to any number of containers
    for i in range(0, 6600):
        containers.append(randomContainer())
    return set(containers)


def writeContainersToFile(containers):
    file = open("containers.csv", "w")
    for container in containers:
        file.write(str(container.getId()) + "\t" + str(container.getLength()) +
                   "\t" + str(container.getWeight()) + "\t" + str(container.getFreight()) +"\t" + str(container.getTotalWeight()) + "\n")


def readContainersFromFile():
    containers = []
    file = open("containers.csv", "r")
    for line in file:
        line = line.split("\t")
        containers.append(Container(int(line[1]), int(
            line[2]), int(line[3]), int(line[0])))
    return containers



class Ship:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.containers = dict()  # For å finne container objekter lettere
        self.containerBay = [
            [[0 for j in range(width)] for i in range(length)] for k in range(height)]
        # width, lenght, height
        # containerBay[0] = height, containerBay[0][0] = length, containerBay[0][0][0] = width


    def getNumberOfContainers(self):
        return len(self.containers)

    def printNice(self):
        for i in range(0, self.height):
            line = ""
            print("Layer " + str(i))
            for j in range(0, self.length):
                line += "\n Row " + str(j+1) + ": "
                for k in range(0, self.width):
                    if isinstance(self.containerBay[i][j][k], Container):
                        line += str(self.containerBay[i]
                                    [j][k].getLength()) + " "
                    else:
                        line += "0 "
            print(line)

    def printPosition(self):
        for i in range(0, self.height):
            line = ""
            print("Layer " + str(i))
            print("Height \t Length \t Width")
            for j in range(0, self.length):
                line += "\n Row " + str(j) + ": "
                for k in range(0, self.width):
                    if isinstance(self.containerBay[i][j][k], Container):
                        line += str(self.containerBay[i][j][k].getPosition()) + " "
                    else:
                        line += "0 "
            print(line)

    def getLength(self):
        return self.length
    
    def getContainerBay(self):
        return self.containerBay

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getContainersDict(self):
        return self.containers

    def getContainers(self):
        return self.containers.values()

    def getContainerDict(self, id):
        return self.getContainersDict().get(id)

    def addContainerToDict(self, container):
        self.containers[container.getId()] = container

    # Testet
    def placeFirstAvailableSpot(self, container,cranes):
        sizeNeeded = container.getLength()
        Continue = True
        if self.findLastSpot() == 0:
            for i in range(0, self.height):
                if Continue:
                    for j in range(cranes, self.length):
                        if Continue:
                            for k in range(0, self.width):
                                if Continue:
                                    if self.containerBay[i][j][k] == 0:
                                        if sizeNeeded == 40:
                                            try:
                                                if self.containerBay[i][j][k+1] == 0:
                                                    # Check if container below is not empty
                                                    try:
                                                        if i > 0:
                                                            if self.containerBay[i-1][j][k] != 0 and self.containerBay[i-1][j][k+1] != 0:
                                                                self.containerBay[i][j][k] = container
                                                                self.containerBay[i][j][k +
                                                                                        1] = container
                                                                container.setPosition(
                                                                    [i, j, k])
                                                                Continue = False
                                                                return True
                                                            else:
                                                                print(
                                                                    "Container below is not empty")
                                                        else:
                                                            self.containerBay[i][j][k] = container
                                                            self.containerBay[i][j][k +
                                                                                    1] = container
                                                            container.setPosition(
                                                                [i, j, k])
                                                            Continue = False
                                                            return True
                                                    except IndexError:
                                                        continue
                                            except IndexError:
                                                continue
                                        elif sizeNeeded == 20:
                                            self.containerBay[i][j][k] = container
                                            container.setPosition([i, j, k])
                                            Continue = False
                                            return True
        else:
            pass

    def findLastSpot(self):
        return (self.containerBay[-1][-1][-1] != 0) and self.checkLastLayer()
    
    def checkLastLayer(self):
        for i in range(0, self.length):
            for j in range(0, self.width):
                if self.containerBay[-1][i][j] != 0:
                    return False
        return True
    
    # Testet
    def addContainer(self, container):
        if (self.placeFirstAvailableSpot(container,0)):
            self.addContainerToDict(container)




    # Testet
    def removeContainerFromShip(self, id):
        container = self.getContainerDict(id)
        if container != None:
            # del self.containers[id]
            position = container.getPosition()
            del self.containers[id]
            if container.getLength() == 40:
                self.containerBay[position[0]][position[1]][position[2]] = 0
                self.containerBay[position[0]][position[1]][position[2]+1] = 0
            else:
                self.containerBay[position[0]][position[1]][position[2]] = 0
            self.loadContainersIncreasingWeight("")

            # positionz = position[0]
            #HØYDE LENGDE BREDDE
           
            # while positionz < self.height:
            #     container = self.getContainerDict(id)
            #     try:
            #         if container.getLength() == 40:
            #                 if self.containerBay[positionz+1][position[1]][position[2]] != 0:
            #                     id = self.containerBay[positionz+1][position[1]][position[2]].getId()
            #                     if id != None:
            #                         print("Fjerner ", id)
            #                         del self.containers[id]
            #                         self.containerBay[positionz+1][position[1]][position[2]] = 0
            #                         self.containerBay[positionz+1][position[1]][position[2]+1] = 0
            #                     else:
            #                         id = self.containerBay[positionz+1][position[1]][position[2]-1]
            #                         print("Fjerner ", self.containerBay[id].getPosition() )
            #                         del self.containers[id]
            #                         self.containerBay[positionz+1][position[1]+1][position[2]-1] = 0
            #                         self.containerBay[positionz+1][position[1]+1][position[2]] = 0
            #                     positionz +=1                        
            #         else:
            #                 if self.containerBay[positionz][position[1]][position[2]] != 0:
            #                     id = self.containerBay[positionz][position[1]][position[2]].getId()
            #                     print("Fjerner ", self.containerBay[id].getPosition())
            #                     del self.containers[id]
            #                     self.containerBay[positionz][position[1]][position[2]] = 0
            #                     positionz +=1
            # # kommer av at vi er på feil side av containeren når vi prøver å fjerne den
            #     except AttributeError or IndexError:
            #         print("IndexError")
            #         self.containerBay[positionz+1][position[1]+1][position[2]-1] = 0
            #         self.containerBay[positionz+1][position[1]+1][position[2]] = 0
            #         positionz+=1
            #         continue
                    
            # print("Removed container from " + str(position))
            # Need to reshuffle containers
            # self.reshuffleContainers()

    # Testet
    # Reshufle when removing a container from the ship

    def reshuffleContainers(self):
        self.containerBay = [
            [[0 for j in range(self.getWidth())] for i in range(self.getLength())] for k in range(self.getHeight())]
        for container in self.getContainers():
            self.placeFirstAvailableSpot(container,0)

    def writeLoadedContainersToFile(self):
        file = open("loadedContainers.csv", "w")
        for container in self.getContainers():
            file.write(str(container.getId()) + "\t" + str(container.getLength()) +
                       "\t" + str(container.getWeight()) + "\t" + str(container.getFreight()) + "\n")

    def readLoadedContainersFromFile(self):
        file = open("loadedContainers.csv", "r")
        for line in file:
            line = line.split("\t")
            container = Container(int(line[1]), int(
                line[2]), int(line[3]), int(line[0]))
            self.addContainer(container)

    def loadContainersFromSet(self, containers):
        # Stack
        orderedList = []
        for container in containers:
            self.addContainer(container)
            orderedList.append(container)
        return orderedList

    def unloadContainersToSet(self):
        # Stack
        orderedList = []
        containers = list(self.getContainers())
        for container in containers:
            self.removeContainerFromShip(container.getId())
            orderedList.append(container)
        return orderedList

    def removeAllContainersFromShip(self):
        containers = list(self.getContainers())
        for container in containers:
            self.removeContainerFromShip(container.getId())

    def loadContainersIncreasingWeight(self, containers):
        if len(containers) == 0:
            liste = list(self.getContainers())
            self.resetLoadedContainers()
        else:
            liste = list(containers)
        liste.sort(key=lambda x: x.getTotalWeight(), reverse=True)
        for container in liste:
            self.addContainer(container)

    def calculateTotalContainerWeightLoaded(self):
        totalWeight = 0
        for container in self.getContainers():
            totalWeight += container.getTotalWeight()
        return totalWeight

    # Starboard høyre
    # PortSide venstre
    def calculateTotalContainerWeightStarboard(self):
        totalWeight = 0
        for container in self.getContainers():
            if container.getPosition()[2] > self.getWidth()/2:
                totalWeight += container.getTotalWeight()
        return totalWeight

    def calculateTotalContainerWeightPortside(self):
        totalWeight = 0
        for container in self.getContainers():
            if container.getPosition()[2] < self.getWidth()/2:
                totalWeight += container.getTotalWeight()
        return totalWeight

    def calculateTotalContainerWeightForward(self):
        totalWeight = 0
        for container in self.getContainers():
            # fra 16 til 22 (7) plasser pos 16 til 22
            if container.getPosition()[1] > self.getLength()*2/3:
                totalWeight += container.getTotalWeight()
        return totalWeight

    def calculateTotalContainerWeightMiddle(self):
        totalWeight = 0
        for container in self.getContainers():
            # 15<=x>=7 pos 8 til 15 (8)
            if container.getPosition()[1] <= self.getLength()*2/3 and container.getPosition()[1] > self.getLength()/3:
                totalWeight += container.getTotalWeight()
        return totalWeight

    def calculateTotalContainerWeightBack(self):
        totalWeight = 0
        for container in self.getContainers():
            # fra 0 -> <8 8plasser pos 0 til 7 (8)
            if container.getPosition()[1] < round(self.getLength()/3):
                totalWeight += container.getTotalWeight()
        return totalWeight
    


    def calculatePercentageStarPort(self):
        try:
            res = round((abs(self.calculateTotalContainerWeightStarboard(
            )-self.calculateTotalContainerWeightPortside())/self.calculateTotalContainerWeightPortside())*100.0, 3)
            print(
                "Percent difference in weight from Starboard to Portside is: " + str(res) + "%")
            return res
        except ZeroDivisionError:
            print("Ship is not loaded properly")


    def calculatePercentageForwardMiddle(self):
        try:
            res = round((abs(self.calculateTotalContainerWeightMiddle(
            )-self.calculateTotalContainerWeightForward())/self.calculateTotalContainerWeightForward())*100.0, 3)
            print(
                "Percent difference in weight from Forward to Middle is: " + str(res) + "%")
            return res
        except ZeroDivisionError:
            print("Ship is not loaded properly")

    def calculatePercentageForwardBack(self):
        try:
            res = round((abs(self.calculateTotalContainerWeightForward(
            )-self.calculateTotalContainerWeightBack())/self.calculateTotalContainerWeightBack())*100.0, 3)
            print(
                "Percent difference in weight from Forward to Back is: " + str(res) + "%")
            return res
        except ZeroDivisionError:
            print("Ship is not loaded properly")

    def calculatePercentageMiddleBack(self):
        try:
            res = round((abs(self.calculateTotalContainerWeightMiddle(
            )-self.calculateTotalContainerWeightBack())/self.calculateTotalContainerWeightBack())*100.0, 3)
            print(
                "Percent difference in weight from Middle to Back is: " + str(res) + "%")
            return res
        except ZeroDivisionError:
            print("Ship is not loaded properly")

    def resetLoadedContainers(self):
        self.containerBay = [
            [[0 for j in range(self.width)] for i in range(self.length)] for k in range(self.height)]
        self.containers = dict()

    def reBalanceContainers(self,containers, randval):
        self.resetLoadedContainers()
        # list(containers).sort(key=lambda x: x.getTotalWeight())
        # random.randint(1, 40)
        for i in range(randval):
            totW = 0
            exec(f'container{i} = list(containers)[i::{randval}]')
            # for j in (eval(f'container{i}')):
            #     totW += j.getTotalWeight()
            # print(totW)
            self.loadContainersIncreasingWeight(eval(f'container{i}'))
        print(randval)

    def reBalanceUntilStable(self):
        containers = self.getContainers()
        randval = 1  # 54 nice?
        while self.calculatePercentageForwardMiddle() >= 10 or self.calculatePercentageForwardBack() >= 10 or self.calculatePercentageMiddleBack() >= 10 or self.calculatePercentageStarPort() >= 5:
            print("Rebalancing")
            randval += 1
            self.reBalanceContainers(containers,randval)

    def checkLayerWeight(self, layer):
        totW = 0
        for i in range(self.length):
            for j in range(self.width):
                if self.containerBay[layer][i][j] != 0:
                    totW += self.containerBay[layer][i][j].getTotalWeight()
        return totW

    def checkAllLayerWeight(self):
        for i in range(self.height):
            print(str(self.checkLayerWeight(i)) + " layer" + str(i))

    def findHeaviestContainers(self, containers):
        popped = []
        containers = list(containers)
        readyToPlace = []
        readyToPlace.append(containers.pop())

        for i in range(len(containers)):
            w = containers[i].getTotalWeight()
            try:
                while w > readyToPlace[-1].getTotalWeight():
                    popped.append(readyToPlace.pop())
                readyToPlace.append(containers[i])
                for j in range(len(popped)):
                    readyToPlace.append(popped.pop())
            except IndexError:
                readyToPlace.append(containers[i])
        return readyToPlace
    

    def loadWithCranes(self, numberOfCranes):
        time = 0
        costInTime = 4 # per container
        self.containerBay = [
            [[0 for j in range(self.width)] for i in range(self.length)] for k in range(self.height)]
        # place containers in bay in different sections of the ship according to numberOfCranes
        # 1 crane = 1 section
        #section is the length of the ship divided by the number of cranes

        #This function works with 4 cranes, if 1 crane, replace with 0 in the place function
        start = []
        for i in range(self.length):
            start.append(((i % 6) * 4 + (i // 6)))
        if numberOfCranes == 1:
            start = [0]*self.length
        j = 0
        for cont in self.getContainers():
            self.placeFirstAvailableSpot(cont,start[j])
            time += costInTime
            j += 1
            if j == 22:
                j = 0
        time = time/numberOfCranes
        print("Time taken to load ship with " + str(numberOfCranes) + " cranes is " + str(time) + " minutes")



                
            

#Takes 4 minutes to load/unload a container



def main():
        
    # rand = randomContainers()
    # writeContainersToFile(rand)


    start = timeit.default_timer()

    # Your statements here


    newShip = Ship(23, 22, 18)
    containers = randomContainers()
    newShip.loadContainersIncreasingWeight(containers)
    newShip.printNice()
    print(newShip.calculateTotalContainerWeightLoaded(), "Total weight")
    #newShip.writeLoadedContainersToFile()
    #newShip.readLoadedContainersFromFile()
    newShip.loadWithCranes(4)
    newShip.loadWithCranes(1)


    # newShip.printPosition()

    # print(newShip.containers)
    # print( " ID  140441490413536" , " POS", newShip.containers.get(140441490413536).getPosition())
    # newShip.printPosition()


    # print(newShip.findHeaviestContainers(containers))
    # print(newShip.printNice())
    # print(newShip.containers.get(140171101967296))
    # newShip.removeContainerFromShip(140171101967296)
    # print(newShip.printNice())
    # print(newShip.printNice())

    # print(newShip.calculatePercentageStarPort())
    # print(newShip.calculatePercentageForwardBack())
    # print(newShip.calculatePercentageForwardMiddle())
    # print(newShip.calculatePercentageMiddleBack())
    (newShip.checkAllLayerWeight())


    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    print(str(newShip.calculateTotalContainerWeightForward()) + "Fremme")
    print(str(newShip.calculateTotalContainerWeightMiddle()) + "Midten")
    print(str(newShip.calculateTotalContainerWeightBack()) + "Bak")

    print(str(newShip.calculateTotalContainerWeightStarboard()) + "Starboard")
    print(str(newShip.calculateTotalContainerWeightPortside()) + "Portside")


    print(newShip.calculatePercentageStarPort())
    print(newShip.calculatePercentageForwardBack())
    print(newShip.calculatePercentageForwardMiddle())
    print(newShip.calculatePercentageMiddleBack())

    # newShip.reBalanceUntilStable()


    # newShip = Ship(23LENGDE, 22BREDDE, 18HØYDE)
    # newShip.addContainer(randomContainer())
    # print(newShip.getContainers())
main()