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

    def getId(self):
        return self.id
    
    def getProcessTime(self):
        return self.processTime

    def getLoadBuffer(self):
        return self.loadBuffer

    def getUnloadBuffer(self):
        return self.unloadBuffer
    
    def getCurrentlyProcessingBatch(self):
        return self.currentlyProcessingBatch
    
    def calculateProcessTime(self, batch):
        totalTime = (self.getProcessTime() * batch.getBatchSize())
        return totalTime

    def getUnloadBufferCapacity(self):
        return self.getUnloadBuffer().getCapacity()

            
    def processBatch(self, batch):
        self.currentlyProcessing = self.getLoadBuffer().removeAndGetBatch(batch)
        time = self.calculateProcessTime(self.currentlyProcessing)
        return time
    
    def getCurrentlyProcessingBatch(self):
        return self.currentlyProcessingBatch
    
    def setCurrentlyProcessingBatch(self, batch):
        self.currentlyProcessingBatch = batch
    
    def getNextTask(self):
        return self.getId() + 1




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

    def canProcessBatch(self,task):
        unloadBufferCap = task.getUnloadBufferCapacity()
        if task.getLoadBuffer() and task.getCurrentlyProcessingBatch() == None and self.getCurrentlyProcessingTask() == None:
            for batch in task.getLoadBuffer().getBatches():
                if batch.getBatchSize() <= unloadBufferCap:
                    return True, batch
        return False, None


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
    
    def getEventAction(self):
        return self.action
    
    def getEventUnit(self):
        return self.unit


class ProductionLine:
    def __init__(self) -> None:

        self.buffer1=Buffer(1,120)
        self.buffer2=Buffer(2,120)
        self.buffer3=Buffer(3,120)
        self.buffer4=Buffer(4,120)
        self.buffer5=Buffer(5,120)
        self.buffer6=Buffer(6,120)
        self.buffer7=Buffer(7,120)
        self.buffer8=Buffer(8,120)
        self.buffer9=Buffer(9,120)
        self.buffer10=Buffer(10,999999)

        self.task1 = Task(1,0.5, self.buffer1, self.buffer2)
        self.task2 = Task(2,3.5, self.buffer2, self.buffer3)
        self.task3 = Task(3,1.2, self.buffer3, self.buffer4)
        self.task4 = Task(4,3, self.buffer4, self.buffer5)
        self.task5 = Task(5,0.8, self.buffer5, self.buffer6)
        self.task6 = Task(6,0.5, self.buffer6, self.buffer7)
        self.task7 = Task(7,1, self.buffer7, self.buffer8)
        self.task8 = Task(8,1.9, self.buffer8, self.buffer9)
        self.task9 = Task(9,0.3, self.buffer9, self.buffer10)

        self.tasks = [self.task1,self.task2,self.task3,self.task4,self.task5,self.task6,self.task7,self.task8,self.task9]

        self.unit1 = Unit(1,[self.task1,self.task3,self.task6,self.task9])
        self.unit2 = Unit(2,[self.task2,self.task5,self.task7])
        self.unit3 = Unit(3,[self.task4,self.task8])

        self.units = [self.unit1, self.unit2, self.unit3]


    def getUnits(self):
        return self.units
    
    def getUnitFromTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
    
    def getTaskFromId(self, id):
        for unit in self.units:
            for task in unit.getTasks():
                if task.getId() == id:
                    return task
    
    def getUnitFromTaskId(self, id):
        for unit in self.units:
            for task in unit.getTasks():
                if task.getTaskId() == id:
                    return unit
        

class Simulation:

    def __init__(self) -> None:
        self.eventqueue = []
        self.batches = []
        self.currentTime = 0
        self.productionLine = ProductionLine()
        self.units = self.productionLine.getUnits()
    
    def getEventQueue(self):
        return self.eventqueue
    
    def getBatches(self):
        return self.batches
    
    def getCurrentTime(self):
        return self.currentTime

    def getProductionLine(self):
        return self.productionLine
    
    def getUnits(self):
        return self.units
    
    def getFirst(self):
        return self.eventqueue[0]
    
    def setCurrentTime(self, time):
        self.currentTime = time

    def createBatches(self):
        wafersToProduce = 1000
        index = 0
        while wafersToProduce > 0:
            batch = Batches(index)
            wafersToProduce -= batch.getBatchSize()
            self.batches.append(batch)
            heapq.heappush(self.eventqueue, Event(0, "loadBatchesToSimulation", self.productionLine.getUnits()[0]))
            index += 1

    def runSimulation(self):
        unit1 = self.productionLine.getUnits()[0]
        task1 = unit1.getTasks()[0]
        self.createBatches()


        while self.getEventQueue():
            self.setCurrentTime(self.getFirst().getEventTime())
            currentEvent = self.eventqueue.pop(0)
            currentUnit = currentEvent.getEventUnit()
            if currentUnit == None:
                continue

            #load batches to simulation
            #--------------------------
            if currentEvent.getEventAction() == "loadBatchesToSimulation":
                if(len(self.batches) == 0):
                    continue
                if task1.getLoadBuffer().canInsertBatch(self.batches[0]):
                    task1.getLoadBuffer().insertBatch(self.batches.pop(0))
                    heapq.heappush(self.getEventQueue(), Event(self.getCurrentTime(), "load", unit1))
                    #print(f"loaded batch to sim at time {self.getCurrentTime()}")
                    #print(f"batches left to load: {len(self.batches)}-------------------------------------------")
                else:
                    heapq.heappush(self.getEventQueue() , Event(self.getCurrentTime() + 60, "loadBatchesToSimulation", unit1))

            #load batches to a task
            # --------------------------              
            if currentEvent.action == "load":
                for task in currentUnit.getTasks():
                    bool, batch = currentUnit.canProcessBatch(task) 
                    if bool:
                        time = task.processBatch(batch) 
                        currentUnit.setCurrentlyProcessingTask(task)
                        currentUnit.getCurrentlyProcessingTask().setCurrentlyProcessingBatch(batch)
                        heapq.heappush(self.getEventQueue(),Event(self.getCurrentTime() + time, "unload", currentUnit))
                        if batch.getId() == 0:
                            print(f"loaded batch {batch.getId()} to Task {task.getId()} at time {self.getCurrentTime()}")
                    else:
                        #print(f"could not load batch to Task {task.getId()}")
                        pass
                           

            #unload batches from a task
            # --------------------------    
            if currentEvent.action == "unload":
                currentTask = currentUnit.getCurrentlyProcessingTask()
                if currentTask == None:
                    continue
                nextTask = self.productionLine.getTaskFromId(currentTask.getNextTask())
                nextTaskUnit = self.productionLine.getUnitFromTask(nextTask)
                batch = currentTask.getCurrentlyProcessingBatch()
                currentTask.getUnloadBuffer().insertBatch(batch)             
                currentUnit.getCurrentlyProcessingTask().setCurrentlyProcessingBatch(None)
                currentUnit.setCurrentlyProcessingTask(None)
                heapq.heappush(self.eventqueue,Event(self.currentTime + 0, "load", currentUnit))
                heapq.heappush(self.eventqueue,Event(self.currentTime + 60, "load", nextTaskUnit))
                if batch.getId() == 0:
                    print(f"unloaded batch {batch.getId()} from Task {currentTask.getId()} at time {self.currentTime}")
        
            if(self.currentTime > 5000):
                print("Simulation finished")
                return
        batch_ids = [batch.getId() for batch in self.productionLine.buffer10.getBatches()]
        print(f"Ids of batches in last buffer: {batch_ids}")
# main          
# ----

def main():
    sim = Simulation()
    sim.runSimulation()
    


main()
