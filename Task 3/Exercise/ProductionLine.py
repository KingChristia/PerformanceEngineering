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

    def __init__(self, identifier) -> None:
        self.identifier = identifier
        self.size = 50#random.randint(20, 50)

        self.taskRemaining = list(range(1, 10))

    def getIdentifier(self):
        return self.identifier

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

    def __init__(self, capacity) -> None:
        # Capacity is 120, unless it is the last one
        # self.capacity = 120 if not last else sys.maxsize
        self.capacity = 120 if capacity == None else capacity
        self.batches = []
        # Decides if it is the last buffer
        # self.last = last

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

    # Kanskje ha en unload funksjon her for å flytte batchen til neste buffer?


class Task:
    TASK_1 = 0.5
    TASK_2 = 3.5
    TASK_3 = 1.2
    TASK_4 = 3
    TASK_5 = 0.8
    TASK_6 = 0.5
    TASK_7 = 1
    TASK_8 = 1.9
    TASK_9 = 0.3

    def __init__(self, task, taskNr) -> None:
        self.task = task
        self.taskNr = taskNr
        self.processTime = 0
        self.input_buffer = Buffer(None)
        self.currentlyProcessing = None

        if taskNr == 9:
            self.output_buffer = Buffer(sys.maxsize)

    def getTask(self):
        return self.task

    def getTasknr(self):
        return self.taskNr

    def getBuffer(self):
        return self.input_buffer

    def getNextTask(self):
        return self.nextTask

    def getProcessTime(self):
        return self.processTime

    def calculateProcessTime(self, batch):
        self.processTime = (self.task * batch.getBatchSize())
        return self.processTime

    def getNextBufferCapacity(self, task):
        return task.getBuffer().getCapacity()
    
    def canProcessBatch(self):
        #print("NextTask ", self.getNextTask().getTasknr(), "TaskNr ", self.getTasknr())
        nextBufferCap = self.getNextTask().getBuffer().getCapacity() if self.getNextTask() != None else sys.maxsize
        # print(nextBufferCap, "Chris")
        if self.getBuffer().getBufferLoad()>0 and self.currentlyProcessing == None:
            for batch in self.input_buffer.getBatches():
                if batch.getBatchSize() <= nextBufferCap and batch.getNextTask() == self.getTasknr():
                    return True, batch
        return False, None
            
    def processBatch(self, batch):
        # print(f"Processing Batch {batch.getIdentifier()} in Task {self.taskNr}")
        self.currentlyProcessing = self.input_buffer.removeAndGetBatch(batch)
        self.currentlyProcessing.removeDoneTask()
        time = self.calculateProcessTime(self.currentlyProcessing)
        return time
    
    def getCurrentlyProcessingBatch(self):
        return self.currentlyProcessing
    
    def setCurrentlyProcessingBatch(self, batch):
        self.currentlyProcessing = batch
        
    


class Unit:

    def __init__(self, identifier, tasks) -> None:
        self.identifier = identifier
        self.tasks = [Task(task[0], task[1]) for task in tasks]
        self.currentlyProcessingTask = None

    def getIdentifier(self):
        return self.identifier

    def getTasks(self):
        return self.tasks
    
    def setCurrentlyProcessingTask(self, task):
        self.currentlyProcessingTask = task

    def getCurrentlyProcessingTask(self):
        return self.currentlyProcessingTask


class Event:
    def __init__(self, time, action, unit) -> None:
        self.time = time
        self.action = action
        self.unit = unit

    def __lt__(self,other):
        return self.time < other.time

    def __eq__(self,other):
        return self.time == other.time

    def getTime(self):
        return self.time
    
    def getUnit(self):
        return self.unit


class ProductionLine:
    def __init__(self) -> None:

        self.units = [Unit("Unit 1", [[Task.TASK_1, 1], [Task.TASK_3, 3], [Task.TASK_6, 6], [Task.TASK_9, 9]]),
                      Unit("Unit 2", [[Task.TASK_2, 2], [Task.TASK_5, 5], [Task.TASK_7, 7]]),
                      Unit("Unit 3", [[Task.TASK_4, 4], [Task.TASK_8, 8]])]
        self.wafersToProduce = 1000
        self.connect_tasks()

    def connect_tasks(self):
        all_tasks = []
        for unit in self.units:
            all_tasks.extend(unit.getTasks())

        all_tasks.sort(key=lambda t: t.getTasknr())

        for i in range(len(all_tasks) - 1):
            all_tasks[i].nextTask = all_tasks[i + 1]
        all_tasks[-1].nextTask = None

    def getUnits(self):
        return self.units
    
    def getUnitFromTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
        return None
        


class Schedule:
    def __init__(self, tasks):
        self.tasks = tasks


class Printer:
    def __init__(self):
        self.separator = "\t"


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
