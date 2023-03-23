# TPK4186 - 2023 - Assignment 1

# 1. Imported modules
# -------------------

import sys
import random

# 2. Containers
# -------------

def Container_New(serialNumber, length, weight, cargo):
    # Require: 0 <= cargo <= 22
    return [serialNumber, length, weight, cargo]

def Container_NewSmall(serialNumber, cargo):
    return Container_New(serialNumber, 20, 2, cargo)

def Container_NewBig(serialNumber, cargo):
    return Container_New(serialNumber, 40, 4, cargo)

def Container_GetSerialNumber(container):
    return container[0]

def Container_SetSerialNumber(container, serialNumber):
    container[0] = serialNumber
    
def Container_GetLength(container):
    return container[1]

def Container_SetLength(container, length):
    container[1] = length

def Container_GetWeight(container):
    return container[2]

def Container_SetWeight(container, weight):
    container[2] = weight

def Container_GetCargo(container):
    return container[3]

def Container_SetCargo(container, cargo):
    container[3] = cargo
    
def Container_GetTotalWeight(container):
    return Container_GetWeight(container) + Container_GetCargo(container)

# 3. Ships
# --------

def Ship_New(length, width, height):
    return [length, width, height, [], dict()]
    
def Ship_GetLength(ship):
    return ship[0]

def Ship_SetLength(ship, length):
    ship[0] = length

def Ship_GetWidth(ship):
    return ship[1]

def Ship_SetWidth(ship, width):
    ship[1] = width

def Ship_GetHeight(ship):
    return ship[2]

def Ship_SetHeight(ship, height):
    ship[2] = height

def Ship_GetContainers(ship):
    return ship[3]

def Ship_GetNumberOfContainers(ship):
    return len(Ship_GetContainers(ship))

def Ship_GetNthContainer(ship, index):
    containers = Ship_GetContainers(ship)
    return containers[index]

def Ship_GetContainerDictionary(ship):
    return ship[4]

def Ship_InsertContainer(ship, container, index):
    containers = Ship_GetContainers(ship)
    containers.insert(index, container)
    Ship_AddContainerToDictionary(ship, container)

def Ship_AppendContainer(ship, container):
    containers = Ship_GetContainers(ship)
    containers.append(container)
    Ship_AddContainerToDictionary(ship, container)

def Ship_LookForContainer(ship, serialNumber):
    containerDictionary = Ship_GetContainerDictionary(ship)
    return containerDictionary.get(serialNumber, None)

def Ship_AddContainerToDictionary(ship, container):
    containerDictionary = Ship_GetContainerDictionary(ship)
    serialNumber = Container_GetSerialNumber(container)
    containerDictionary[serialNumber] = container

def Ship_RemoveContainerFromDictionary(ship, container):
    containerDictionary = Ship_GetContainerDictionary(ship)
    serialNumber = Container_GetSerialNumber(container)
    del containerDictionary[serialNumber]

def Ship_LoadContainer(ship, newContainer):
    newContainerWeight = Container_GetTotalWeight(newContainer)
    loaded = False
    i = 0
    while i<Ship_GetNumberOfContainers(ship):
        container = Ship_GetNthContainer(ship, i)
        containerWeight = Container_GetTotalWeight(container)
        if containerWeight<=newContainerWeight:
            Ship_InsertContainer(ship, newContainer, i)
            loaded = True
            break
        i = i + 1
    if not loaded:
        Ship_AppendContainer(ship, newContainer)

def Ship_IsEmpty(ship):
     return Ship_GetNumberOfContainers(ship)==0
   
def Ship_PushContainer(ship, container):
    containers = Ship_GetContainers(ship)
    containers.append(container)
    Ship_AddContainerToDictionary(ship, container)

def Ship_PushContainers(ship, containers):
    while len(containers)!=0:
        container = containers.pop()
        Ship_PushContainer(ship, container)
    
def Ship_PopContainer(ship):
     if Ship_GetNumberOfContainers(ship)==0:
         return
     containers = Ship_GetContainers(ship)
     container = containers.pop()
     Ship_RemoveContainerFromDictionary(ship, container)

def Ship_PopLighterContainers(ship, thresholdWeight):
    poppedContainers = []
    while not Ship_IsEmpty(ship):
        container = Ship_GetTopContainer(ship)
        totalWeight = Container_GetTotalWeight(container)
        if totalWeight>=thresholdWeight:
            break
        Ship_PopContainer(ship)
        poppedContainers.append(container)
    return poppedContainers

def Ship_GetTopContainer(ship):
     if Ship_GetNumberOfContainers(ship)==0:
         return None
     containers = Ship_GetContainers(ship)
     return containers[-1]

def Ship_PileContainer(ship, container):
    totalWeightContainer = Container_GetTotalWeight(container)
    poppedContainers = Ship_PopLighterContainers(ship, totalWeightContainer)
    Ship_PushContainer(ship, container)
    Ship_PushContainers(ship, poppedContainers)
 

# 4: Printer and Reader
# ---------------------

def Printer_ExportShip(ship, fileName, separator):
    outputFile = open(fileName, "w")
    Printer_PrintShip(ship, outputFile, separator)
    outputFile.close()

def Printer_PrintContainer(container, outputFile, separator):
    serialNumber = Container_GetSerialNumber(container)
    length = Container_GetLength(container)
    weight = Container_GetWeight(container)
    cargo = Container_GetCargo(container)
    totalWeight = Container_GetTotalWeight(container)
    outputFile.write(str(serialNumber))
    outputFile.write(separator + str(length))
    outputFile.write(separator + str(weight))
    outputFile.write(separator + str(cargo))
    outputFile.write(separator + str(totalWeight) + "\n")

def Printer_PrintShip(ship, outputFile, separator):
    length = Ship_GetLength(ship)
    width = Ship_GetWidth(ship)
    height = Ship_GetHeight(ship)
    containers = Ship_GetContainers(ship)
    outputFile.write("Ship\n")
    outputFile.write("length" + separator + str(length) + "\n")
    outputFile.write("width" + separator + str(width) + "\n")
    outputFile.write("height" + separator + str(height) + "\n")
    outputFile.write("Containers\n")
    for container in containers:
        Printer_PrintContainer(container, outputFile, separator)

def Reader_ImportShip(fileName, separator):
    inputFile = open(fileName, "r")
    ship = Reader_LoadShip(inputFile, separator)
    inputFile.close()
    return ship

def Reader_LoadShip(inputFile, separator):
    line = next(inputFile)
    line = next(inputFile)
    line = line.rstrip()
    tokens = line.split(separator)
    length = int(tokens[1])
    line = next(inputFile)
    line = line.rstrip()
    tokens = line.split(separator)
    width = int(tokens[1])
    line = next(inputFile)
    line = line.rstrip()
    tokens = line.split(separator)
    height = int(tokens[1])
    ship = Ship_New(length, width, height)
    line = next(inputFile)
    for line in inputFile:
        container = Reader_LoadContainer(line, separator)
        Ship_LoadContainer(ship, container)
    return ship

def Reader_LoadContainer(line, separator):
    line = line.rstrip()
    tokens = line.split(separator)
    serialNumber = tokens[0]
    length = int(tokens[1])
    weight = int(tokens[2])
    cargo = int(tokens[3])
    container = Container_New(serialNumber, length, weight, cargo)
    return container


# 5. Container Manager
# --------------------

ContainerManager_year = 2023
ContainerManager_month = 1
ContainerManager_day = 27
ContainerManager_number = 0

def ContainerManager_NewSerialNumber():
    global ContainerManager_year
    global ContainerManager_month
    global ContainerManager_day
    global ContainerManager_number
    ContainerManager_number += 1
    serialNumber = "{0:d}-{1:02d}-{2:d}-{3:04d}".format( \
        ContainerManager_year, ContainerManager_month, ContainerManager_day, ContainerManager_number)
    return serialNumber

def ContainerManager_NewRandomContainer():
    serialNumber = ContainerManager_NewSerialNumber()
    isSmall = random.randint(0, 1)
    if isSmall==0:
        cargo = random.randint(0, 20)
        container = Container_NewSmall(serialNumber, cargo)
    else:
        cargo = random.randint(0, 22)
        container = Container_NewBig(serialNumber, cargo)
    return container
   

# X. Main
# -------

# ship = Ship_New(23, 22, 18)
# for i in range(0, 100):
#     container = ContainerManager_NewRandomContainer()
#     Ship_PileContainer(ship, container)

# Printer_PrintShip(ship)

# container = Ship_LookForContainer(ship, "2023-01-27-0061")
# if container==None:
#     print("No such container")
# else:
#     Printer_PrintContainer(container, sys.stdout, " ")

# Printer_PrintShip(ship, sys.stdout, " ")

# Printer_ExportShip(ship, "myShip.csv", ";")

ship = Reader_ImportShip("myShip.csv", ";")
Printer_PrintShip(ship, sys.stdout, " ")













