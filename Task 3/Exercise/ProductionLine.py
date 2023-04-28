# Unit can only perform one task at a time
# Batch size can vary from 20 to 50 wafers
# Loading from input buffer to machine takes 1 minute = 60 seconds.
# Unloading from machine to next buffer takes also 1 minute = 60 seconds.
# Batches must be unloaded as soon as they are produced.
# Buffers cannot contain more tahn 120 wafers, unless the last one, that is inf


""" 
   Objective is to design a simulator for a production line, and to optimize the production. Produce 1000 wafers in the shortest time possible. 
"""
# 1. Imported Modules
# --------------------
from collections import deque
import random
import sys
import heapq

# 2. Batches
# -----------


class Batches:

    def __init__(self, id):
        self.id = id
        self.size = 50

    def getId(self):
        return self.id

    def getBatchSize(self):
        return self.size
    
    def getTasksRemaining(self):
        return self.taskRemaining

    def getNextTask(self):
        return self.taskRemaining[0]

    def removeDoneTask(self):
        self.taskRemaining.remove(self.getNextTask())


# 3. Buffers
# -----------


class Buffer:
    LOADING_TIME = 60
    UNLOADING_TIME = 60

    def __init__(self, id,capacity):

        self.id = id
        self.capacity = capacity
        self.batches = []

    def getId(self):
        return self.id
    
    def getCapacity(self):
        return self.capacity

    def getBatches(self):
        return self.batches

    def getBufferLoad(self):
        size = 0
        for batch in self.batches:
            size += batch.getBatchSize()
        return size

    def insertBatch(self, batch):
        if self.getBufferLoad() + batch.getBatchSize() > self.capacity:
            print("Not enough space in buffer")
            return
        self.batches.append(batch)

    def canInsertBatch(self, batch):
        if self.getBufferLoad() + batch.getBatchSize() > self.capacity:
            return False
        return True

    def removeAndGetBatch(self, batch):
        self.batches.remove(batch)
        return batch

    def popBatch(self):
        return self.batches.pop(0)


class Task:
    def __init__(self, id,processTime, loadBuffer,unloadBuffer):
        self.id = id
        self.processTime = processTime
        self.loadBuffer = loadBuffer
        self.unloadBuffer = unloadBuffer
        self.currentlyProcessingBatch = None

    def getTaskId(self):
        return self.task
    
    def getProcessTime(self):
        return self.processTime

    def getLoadBuffer(self):
        return self.loadBuffer

    def getUnloadBuffer(self):
        return self.unloadBuffer

    def calculateProcessTime(self, batch):
        totalTime = (self.getProcessTime() * batch.getBatchSize())
        return totalTime

    def getUnloadBufferCapacity(self, task):
        return self.getUnloadBuffer().getCapacity()
    
    def canProcessBatch(self):
        unloadBufferCap = self.getUnloadBufferCapacity()
        if self.getLoadBuffer() and self.currentlyProcessing == None:
            for batch in self.getLoadBuffer().getBatches():
                if batch.getBatchSize() <= unloadBufferCap:
                    return True, batch
        return False, None
            
    def processBatch(self, batch):
        self.currentlyProcessing = self.input_buffer.removeAndGetBatch(batch)
        time = self.calculateProcessTime(self.currentlyProcessing)

        return time
    
    def getCurrentlyProcessingBatch(self):
        return self.currentlyProcessingBatch
    
    def setCurrentlyProcessingBatch(self, batch):
        self.currentlyProcessingBatch = batch
        


class Unit:

    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks
        self.currentlyProcessingTask = None

    def getId(self):
        return self.id

    def getTasks(self):
        return self.tasks
    
    def getCurrentlyProcessingTask(self):
        return self.currentlyProcessingTask
    
    def setCurrentlyProcessingTask(self, task):
        self.currentlyProcessingTask = task


class Event:
    def __init__(self, time, action, unit) -> None:
        self.time = time
        self.action = action
        self.unit = unit

    def __lt__(self,other):
        return self.time < other.time

    def __eq__(self,other):
        return self.time == other.time

    def getEventTime(self):
        return self.time
    
    def getEventUnit(self):
        return self.unit


class ProductionLine:
    def __init__(self) -> None:

        buffer1=Buffer(1,120)
        buffer2=Buffer(2,120)
        buffer3=Buffer(3,120)
        buffer4=Buffer(4,120)
        buffer5=Buffer(5,120)
        buffer6=Buffer(6,120)
        buffer7=Buffer(7,120)
        buffer8=Buffer(8,120)
        buffer9=Buffer(9,120)
        buffer10=Buffer(10,999999)

        task1 = Task(1,0.5, buffer1, buffer2)
        task2 = Task(2,3.5, buffer2, buffer3)
        task3 = Task(3,1.2, buffer3, buffer4)
        task4 = Task(4,3, buffer4, buffer5)
        task5 = Task(5,0.8, buffer5, buffer6)
        task6 = Task(6,0.5, buffer6, buffer7)
        task7 = Task(7,1, buffer7, buffer8)
        task8 = Task(8,1.9, buffer8, buffer9)
        task9 = Task(9,0.3, buffer9, buffer10)

        unit1 = Unit(1,[task1,task3,task6,task9])
        unit2 = Unit(2,[task2,task5,task7])
        unit3 = Unit(3,[task4,task8])

        self.units = [unit1, unit2, unit3]


    def getUnits(self):
        return self.units
    
    def getUnitFromTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
        

class Simulation:

    def __init__(self) -> None:
        self.eventqueue = []
        self.batches = []
        self.currentTime = 0
        self.productionLine = ProductionLine()
        self.units = self.productionLine.getUnits()
    
    def getFirst(self):
        return self.eventqueue[0]


    # Den funksjonen som er før første input buffer.
    def getProductionLine(self):
        return self.productionLine

    def createBucketOfBatches(self):
        wafersToProduce = 1000
        index = 0
        while wafersToProduce > 0:
            batch = Batches(index)
            wafersToProduce -= batch.getBatchSize()
            self.batches.append(batch)
            heapq.heappush(self.eventqueue, Event(0, "loadBatchesToSimulation", None))
            index += 1

    def getEventQueue(self):
        return self.eventqueue
    
    def setCurrentTime(self, time):
        self.currentTime = time

    def runSimulation(self):
        unit1 = self.productionLine.getUnits()[0]
        unit2 = self.productionLine.getUnits()[1]
        unit3 = self.productionLine.getUnits()[2]
        self.createBucketOfBatches()
        
        while self.getEventQueue():
            # Sjekker eventqueue om neste action er å laste inn til første input
            self.setCurrentTime(self.getFirst().getTime())
            currentEvent = self.eventqueue.pop(0)
            currentUnit = currentEvent.getUnit()
            if currentEvent.action == "loadBatchesToSimulation":
                # Sjekker om det er plass i første inputbuffer
                if self.productionLine.getUnits()[0].getTasks()[0].getBuffer().canInsertBatch(self.batches[0]):
                    # Inserte den i første buffer
                    self.productionLine.getUnits()[0].getTasks()[0].getBuffer().insertBatch(self.batches.pop(0))
                    heapq.heappush(self.eventqueue, Event(self.currentTime, "load", unit1))
                    print(f"loaded batch to sim at time {self.currentTime}")
                else:
                    #ENDRE FRA 60 TIL NOE MINDRE SENERE
                    heapq.heappush(self.eventqueue , Event(self.currentTime + 60, "loadBatchesToSimulation", unit1))
                    print(f"could not load batch to sim at time {self.currentTime}")
                          
            if currentEvent.action == "load":
                for task in currentUnit.getTasks():#Task 1, 3 ,6 ,9 
                    bool, batch = task.canProcessBatch() #sjekker om task kan ta en batch fra bufferen sin
                    if bool: # sjekker buffer før, etter og task
                        time = task.processBatch(batch) #tar en batch fra bufferen sin og kjører den
                        currentUnit.setCurrentlyProcessingTask(task)
                        heapq.heappush(self.eventqueue,Event(self.currentTime + time, "unload", currentUnit)) #lager ny unload event
                        print(f"loaded batch to {currentUnit.getIdentifier()} at time {self.currentTime}")
                    else:
                        pass
                           
                 
            if currentEvent.action == "unload":
                #Sette currentlyProcessing til None igjen
                nextTaskUnit = self.productionLine.getUnitFromTask(currentUnit.getCurrentlyProcessingTask().getNextTask()) #henter neste task sin unit
                """ for task in currentUnit.getTasks():
                    if task.getBuffer().canInsertBatch(currentUnit.getCurrentlyProcessingTask().getCurrentlyProcessingBatch()):
                        task.getBuffer().insertBatch(currentUnit.getCurrentlyProcessingTask().getCurrentlyProcessingBatch()) """
                print(task.getBuffer().getIdentifier())
                currentUnit.getCurrentlyProcessingTask().setCurrentlyProcessingBatch(None)
                currentUnit.setCurrentlyProcessingTask(None)
                heapq.heappush(self.eventqueue,Event(self.currentTime + 0, "load", currentUnit))
                heapq.heappush(self.eventqueue,Event(self.currentTime + 60, "load", nextTaskUnit))
                print(f"unloaded batch from {currentUnit.getIdentifier()} at time {self.currentTime}")
                print(f"buffer 2: {nextTaskUnit.getTasks()[1].getBuffer().getBatches()}")
        
            if(self.currentTime > 1000):
                print("Simulation finished")
                return
# main          
# ----

def main():
    productionLine = ProductionLine()
    sim = Simulation()
    sim.runSimulation()
    


main()
