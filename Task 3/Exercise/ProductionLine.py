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
import DocumentWriter

# 2. Batches
# -----------


class Batches:

    def __init__(self, id, size):
        self.id = id
        self.taskRemaining = list(range(1, 10))
        self.size = random.randint(20, 50) if size == None else size 


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

    def setRandomSize(self,bool):
        self.randomSize = bool


# 3. Buffers
# -----------


class Buffer:
    LOADING_TIME = 60
    UNLOADING_TIME = 60

    def __init__(self, id, capacity):

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
            # Her er bufferen for neste task full
            Exception("Buffer is full")
        self.batches.append(batch)

    def canInsertBatch(self, batch):
        return (self.getBufferLoad() + batch.getBatchSize()) <= self.capacity

    def removeBatch(self, batch):
        self.batches.remove(batch)

    def popBatch(self):
        return self.batches.pop(0)

    def __str__(self):
        return self.id


# 4. Tasks
# ---------
class Task:
    def __init__(self, id, processTime, loadBuffer, unloadBuffer):
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
        return round(self.getProcessTime() * batch.getBatchSize(), 0)

    def getUnloadBufferCapacity(self):
        return self.getUnloadBuffer().getBufferLoad()

    def processBatch(self, batch):
        self.currentlyProcessingBatch = batch
        self.getLoadBuffer().removeBatch(batch)
        return self.calculateProcessTime(self.currentlyProcessingBatch)

    def moveBatch(self, batch):
        self.getUnloadBuffer().getBatches().append(batch)

    def getCurrentlyProcessingBatch(self):
        return self.currentlyProcessingBatch

    def setCurrentlyProcessingBatch(self, batch):
        self.currentlyProcessingBatch = batch

    def getNextTask(self):
        return self.getId() + 1


# 5. Units
# ---------
class Unit:

    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks
        self.currentlyProcessingTask = None
        self.availableAt = 0

    def getId(self):
        return self.id

    def getTasks(self):
        return self.tasks

    def getCurrentlyProcessingTask(self):
        return self.currentlyProcessingTask

    def setCurrentlyProcessingTask(self, task):
        self.currentlyProcessingTask = task

    def getAvailableAt(self):
        return self.availableAt

    def setAvailableAt(self, time):
        self.availableAt == time

    def canProcessBatch(self, task):
        unloadBufferCap = (task.getUnloadBuffer(
        ).getCapacity() - task.getUnloadBufferCapacity())
        if task.getLoadBuffer().getBufferLoad() > 0 and task.getCurrentlyProcessingBatch() == None and self.getCurrentlyProcessingTask() == None:
            for batch in task.getLoadBuffer().getBatches():
                if batch.getBatchSize() <= unloadBufferCap:
                    return True, batch
        return False, None


# 6. Events
# ---------
class Event:
    def __init__(self, time, action, unit) -> None:
        self.time = time
        self.action = action
        self.unit = unit

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time

    def getEventTime(self):
        return self.time

    def getEventAction(self):
        return self.action

    def getEventUnit(self):
        return self.unit


# 7. Production Line
# -------------------
class ProductionLine:
    def __init__(self) -> None:

        self.buffer1 = Buffer(1, 120)
        self.buffer2 = Buffer(2, 120)
        self.buffer3 = Buffer(3, 120)
        self.buffer4 = Buffer(4, 120)
        self.buffer5 = Buffer(5, 120)
        self.buffer6 = Buffer(6, 120)
        self.buffer7 = Buffer(7, 120)
        self.buffer8 = Buffer(8, 120)
        self.buffer9 = Buffer(9, 120)
        self.buffer10 = Buffer(10, 999999)

        self.task1 = Task(1, 0.5, self.buffer1, self.buffer2)
        self.task2 = Task(2, 3.5, self.buffer2, self.buffer3)
        self.task3 = Task(3, 1.2, self.buffer3, self.buffer4)
        self.task4 = Task(4, 3, self.buffer4, self.buffer5)
        self.task5 = Task(5, 0.8, self.buffer5, self.buffer6)
        self.task6 = Task(6, 0.5, self.buffer6, self.buffer7)
        self.task7 = Task(7, 1, self.buffer7, self.buffer8)
        self.task8 = Task(8, 1.9, self.buffer8, self.buffer9)
        self.task9 = Task(9, 0.3, self.buffer9, self.buffer10)

        self.tasks = [self.task1, self.task2, self.task3, self.task4,
                      self.task5, self.task6, self.task7, self.task8, self.task9]

        self.unit1 = Unit(1, [self.task1, self.task3, self.task6, self.task9])
        self.unit2 = Unit(2, [self.task2, self.task5, self.task7])
        self.unit3 = Unit(3, [self.task4, self.task8])

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

    def getTasks(self):
        return self.tasks


# 8. Printer
# ----------
class Printer:
    def __init__(self):
        self.outputfile = sys.stdout
       
    def setOutputFile(self,outputFile):
        self.outputfile = open(outputFile, "w")
        
    def removeOutput(self):
        self.outputfile = None
               
    def getDocumentWriter(self) -> DocumentWriter.DocumentWriter:
        return self.DocumentWriter

    def createDocument(self, filename, title):
        self.DocumentWriter = DocumentWriter.DocumentWriter("Wafer Production Line - Optimization", "Optimization")
        self.DocumentWriter.save()
    
    def getBuffers(self, productionLine):
        if self.outputfile != None:
            for task in productionLine.getTasks():
                print(task.getLoadBuffer().getBatches())
                for batch in task.getLoadBuffer().getBatches():
                    print(f"batch {batch.getId()} in buffer {task.getLoadBuffer().getId()}")
            batch_ids = [batch.getId() for batch in productionLine.buffer10.getBatches()]
            print(f"Ids of batches in last buffer: {batch_ids}")

    def getTasks(self, productionLine,outputFile):
        if self.outputfile != None:
            for task in productionLine.getTasks():
                print(task.getCurrentlyProcessingBatch())

    def printEventQueue(self, eventQueue, outputFile):
        if self.outputfile != None:
            outputFile.write("Waiting Events\n")
            for event in eventQueue.getEventQueue():
                self.printEvent(event, outputFile)

    def printEvent(self, event, outputFile):
        if self.outputfile != None:
            outputFile.write(f"Event: {event.getEventAction()} at {event.getEventTime()} on unit {event.getEventUnit().getId()}\n")

    def printIntroduction(self,simulation,outputFile):
        if self.outputfile != None:
            outputFile.write(f"\nHere is a simulation of {len(simulation.getBatches())} Batches running`\n")
            wafers = 0
            for batch in simulation.getBatches():
                wafers += batch.getBatchSize()
            average = wafers / len(simulation.getBatches())
            outputFile.write(f"The batches are produced randomly and have an average size of {round(average,1)}\n")
            outputFile.write(f"The total runTime is found at the bottom\n\n")
        
        
    def printLoadedToSim(self,batch,event,outputFile):
        if self.outputfile != None:
            outputFile.write(f"Loaded batch {batch.getId()} with size {batch.getBatchSize()} to simulation at time {event.getEventTime()}\n")

    def printLoad(self,batch,task,event,outputFile):
        if self.outputfile != None:
            outputFile.write(f"Loaded batch {batch.getId()} to task {task.getId()} at time {event.getEventTime()}\n")

    def printUnload(self,batch,task,event,outputFile):
        if self.outputfile != None:
            outputFile.write(f"Unloaded batch {batch.getId()} from task {task.getId()} at time {event.getEventTime()}\n")

    def printTotal(self,simulation,outputFile):
        if self.outputFile != None:
            outputFile.write(f"\n\nTotal runtime was ")




# 9. Simulation
# -------------
class Simulation:

    def __init__(self, wafersToProduce) -> None:
        self.eventqueue = []
        self.batches = []
        self.currentTime = 0
        self.productionLine = ProductionLine()
        self.units = self.productionLine.getUnits()
        self.printer = Printer()
        self.wafersToProduce = wafersToProduce
        self.batchSize = None
        self.interval = 0
        self.timebetween = 60

    def getEventQueue(self):
        return self.eventqueue
    
    def getBatchSize(self):
        return self.batchSize
    
    def setBatchSize(self, batchSize):
        self.batchSize = batchSize
    
    def getPrinter(self):
        return self.printer

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
    
    def addBatches(self, batch):
        self.batches.append(batch)
        
    def getBatches(self):
        return self.batches
    
    def addEvent(self, event):
        heapq.heappush(self.getEventQueue(),event)
        
    def getTimeBetweenBatches(self):
        return self.timebetween
    
    def setTimeBetweenBatches(self,time):
        self.timebetween = time
        
    def getInterval(self):
        return self.interval
    
    def setInterval(self, interval):
        self.interval = interval
        
    def createBatches(self):
        index = 0
        
        while self.wafersToProduce > 0:
            batch = Batches(index+1, self.getBatchSize())
            self.wafersToProduce -= batch.getBatchSize()
            self.addBatches(batch)
            heapq.heappush(self.eventqueue, Event(
                self.timebetween, "loadBatchesToSimulation", self.productionLine.getUnits()[0]))
            self.timebetween += self.interval
            index += 1

    def runSimulation(self):
        unit1 = self.productionLine.getUnits()[0]
        unit2 = self.productionLine.getUnits()[1]
        unit3 = self.productionLine.getUnits()[2]
        task1 = unit1.getTasks()[0]
        
        self.createBatches()
        self.printer.printIntroduction(self,self.printer.outputfile)

        while self.getEventQueue():
            self.setCurrentTime(self.getFirst().getEventTime())
            currentEvent = heapq.heappop(self.eventqueue)

            currentUnit = currentEvent.getEventUnit()
            if currentUnit == None:
                continue
            # load batches to simulation
            # --------------------------
            if currentEvent.getEventAction() == "loadBatchesToSimulation":
                if (len(self.batches) == 0):
                    continue
                elif task1.getLoadBuffer().canInsertBatch(self.batches[0]):
                    batch = self.batches.pop(0)
                    task1.getLoadBuffer().insertBatch(batch)
                    heapq.heappush(self.getEventQueue(), Event(
                        self.getCurrentTime(), "load", unit1))
                    self.printer.printLoadedToSim(batch,currentEvent,self.printer.outputfile)
                else:
                    heapq.heappush(self.getEventQueue(), Event(
                    self.getCurrentTime()+1, "loadBatchesToSimulation", unit1))


            # load batches to a task
            # --------------------------
            elif currentEvent.action == "load":
                for task in currentUnit.getTasks():
                    bool, batch = currentUnit.canProcessBatch(task)
                    if bool:
                        time = task.processBatch(batch) + 1
                        currentUnit.setCurrentlyProcessingTask(task)
                        currentUnit.getCurrentlyProcessingTask().setCurrentlyProcessingBatch(batch)
                        currentUnit.setAvailableAt(
                            self.getCurrentTime() + time)
                        heapq.heappush(self.getEventQueue(), Event(
                            self.getCurrentTime() + time, "unload", currentUnit))
                        self.printer.printLoad(batch,task,currentEvent,self.printer.outputfile)
                        continue

            # unload batches from a task
            # --------------------------

            elif currentEvent.action == "unload":
                currentTask = currentUnit.getCurrentlyProcessingTask()

                if currentTask == None:
                    continue

                nextTask = self.productionLine.getTaskFromId(
                    currentTask.getNextTask())

                batch = currentTask.getCurrentlyProcessingBatch()
                currentTask.getUnloadBuffer().insertBatch(batch)
                currentUnit.getCurrentlyProcessingTask().setCurrentlyProcessingBatch(None)
                currentUnit.setCurrentlyProcessingTask(None)
                heapq.heappush(self.eventqueue, Event(
                    self.currentTime + 0, "load", currentUnit))
                self.printer.printUnload(batch,currentTask,currentEvent,self.printer.outputfile)
                # Siste Task på unit 1
                if self.productionLine.getUnitFromTask(nextTask) == None:
                    if len(self.getEventQueue())==0:
                        continue
                    heapq.heappush(self.eventqueue, Event(
                        self.currentTime + 1, "load", unit2))
                    heapq.heappush(self.eventqueue, Event(
                        self.currentTime + 1, "load", unit3))
                else:
                    heapq.heappush(self.eventqueue, Event(
                        self.currentTime + 1, "load", self.productionLine.getUnitFromTask(nextTask)))
                    
        #self.printer.getBuffers(self.productionLine)
        print("Simulation finished", self.currentTime)


# 10. Optimization
def worstCase():
    #Manual to send in one batch at a time
    wafersToProduce = 1000
    index = 0
    totalTime = 0
    #Creating one batch then run the simulation
    while wafersToProduce > 0:
        batch = Batches(index, None)
        simulation = Simulation(batch.getBatchSize())
        wafersToProduce -= batch.getBatchSize()
        index += 1
        simulation.runSimulation()
        totalTime += simulation.getCurrentTime()
    return totalTime

def reducingTimeBetweenBatches():
    numberOfSimulations = 200 #This number changes time between batches
    sim1 = []
    sim2 = []
    sim3 = []
    
    while numberOfSimulations > 0:
        
        #Simulation 1 with batchsize 20
        simulation1 = Simulation(1000)
        simulation1.setBatchSize(20)
        simulation1.getPrinter().removeOutput() #Removes the print that runs every simulation
        simulation1.setInterval(numberOfSimulations) #Increase time between loading with a constant number
        simulation1.setTimeBetweenBatches(0) #Change the loading time between batches to be the same number as simulations
        simulation1.runSimulation()
        sim1.append(simulation1.getCurrentTime())
        
        #Simulation 2 with batchsize 50
        simulation2 = Simulation(1000)
        simulation2.setBatchSize(50)
        simulation2.getPrinter().removeOutput() #Removes the print that runs every simulation
        simulation2.setInterval(numberOfSimulations) #Increase time between loading with a constant number
        simulation2.setTimeBetweenBatches(0) #Change the loading time between batches to be the same number as simulations
        simulation2.runSimulation()
        sim2.append(simulation2.getCurrentTime())
        
        simulation3 = Simulation(1000)
        simulation3.setBatchSize(None)
        simulation3.getPrinter().removeOutput() #Removes the print that runs every simulation
        simulation3.setInterval(numberOfSimulations) #Increase time between loading with a constant number
        simulation3.setTimeBetweenBatches(0) #Change the loading time between batches to be the same number as simulations
        simulation3.runSimulation()
        sim3.append(simulation3.getCurrentTime())
        
        numberOfSimulations -= 1
        
    print(min(sim1))
    print(min(sim2))
    print(min(sim3))

    
        
        
reducingTimeBetweenBatches()
   


def Task_4_OneBatch():
    sim = Simulation(20)
    sim.getPrinter().setOutputFile("OneBatch.txt")
    sim.runSimulation()

def Task_4_FewBatches():
    sim = Simulation(150)
    sim.getPrinter().setOutputFile("FewBatches.txt")
    sim.runSimulation()

def Task_4_AllBatches():
    sim = Simulation(1000)
    sim.getPrinter().setOutputFile("AllBatches.txt")
    sim.runSimulation()
    
    

def Task_5():
    #Worst Case 
    return worstCase()
    
def Optimization():
    printer = Printer()
    printer.createDocument("Wafer Production Line - Optimization", "Optimization")
    
    worstCaseTime = Task_5()
    printer.getDocumentWriter().addHeading("2.3 Optimization",1)
    printer.getDocumentWriter().addHeading("Task 5.",1)
    printer.getDocumentWriter().addHeading("Simulation with Worst Case", 2)
    printer.getDocumentWriter().addParagraph("This is an example of runtime with the worst case solution. One batch is loaded into the simulation, and the next one is not loaded until the first one is finished. This is repeated until all 1000 wafers is produced. The batch sizes is random from 20 to 50 wafers per batch, and therefore some variation in time between each run. The total runtime is: " + str(worstCaseTime) + " minutes for this simulation.")
    
    #Current optimization with reduced loading times
    printer.getDocumentWriter().addHeading("Simulation with reduced loadtime between batches",2)
    
    
    
#Optimization()       

# 10. Main
# --------
def main():
    simulation = Simulation(1000)
    #Task_5()
    simulation.runSimulation()
    #worstCase()


    # sim.printAllBuffers()

    # sim.printAllBuffers()


#main()

Task_4_AllBatches()