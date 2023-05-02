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
import itertools
import random
import sys
import heapq
import time
import DocumentWriter
import matplotlib.pyplot as plt

# 2. Batches
# -----------


class Batch:

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

    def setRandomSize(self, bool):
        self.randomSize = bool


# 3. Buffers
# -----------


class Buffer:

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
    
    def setLoadBuffer(self,buffer):
        self.loadBuffer = buffer

    def getUnloadBuffer(self):
        return self.unloadBuffer
    
    def setUnloadBuffer(self,buffer):
        self.unloadBuffer = buffer

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

    def getId(self):
        return self.id

    def getTasks(self):
        return self.tasks

    def setTasks(self, tasks):
        self.tasks = tasks

    def getCurrentlyProcessingTask(self):
        return self.currentlyProcessingTask

    def setCurrentlyProcessingTask(self, task):
        self.currentlyProcessingTask = task

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

        # self.task1 = Task(1, 0.5)
        # self.task2 = Task(2, 3.5)
        # self.task3 = Task(3, 1.2)
        # self.task4 = Task(4, 3 )
        # self.task5 = Task(5, 0.8)
        # self.task6 = Task(6, 0.5)
        # self.task7 = Task(7, 1 )
        # self.task8 = Task(8, 1.9)
        # self.task9 = Task(9, 0.3)

        #def assignBuffers(self):
        #   for task in self.tasks:
        #       for buffer in self.buffers:
        #           if task.getId() == buffer.getId():
        #               task.setLoadBuffer(buffer)
        #           elif task.getId() == buffer.getId()+1:
        #               task.setUnloadBuffer(buffer)

        self.unit1 = Unit(1, [self.task1, self.task3, self.task6, self.task9])
        self.unit2 = Unit(2, [self.task2, self.task5, self.task7])
        self.unit3 = Unit(3, [self.task4, self.task8])

        # self.unit1 = Unit(1)
        # self.unit2 = Unit(2)
        # self.unit3 = Unit(3)

        #def assignTasksToUnits(self):
        #   self.unit1.setTasks([self.task1, self.task3, self.task6, self.task9])
        #   self.unit1.setTasks([self.task2, self.task5, self.task7])
        #   self.unit1.setTasks([self.task4, self.task8])
        
        self.buffers = [self.buffer1, self.buffer2, self.buffer3, self.buffer4, self.buffer5, self.buffer6, self.buffer7, self.buffer8, self.buffer9, self.buffer10]
        self.tasks = [self.task1, self.task2, self.task3, self.task4,self.task5, self.task6, self.task7, self.task8, self.task9]
        self.units = [self.unit1, self.unit2, self.unit3]

        #assignBuffers()
        #assignTasksToUnits()




    # This only needs to run once
    def generate_task_permutations(self):
        unit1_permutations = list(itertools.permutations(self.unit1.tasks))
        unit2_permutations = list(itertools.permutations(self.unit2.tasks))
        unit3_permutations = list(itertools.permutations(self.unit3.tasks))

        all_permutations = []

        for perm1 in unit1_permutations:
            for perm2 in unit2_permutations:
                for perm3 in unit3_permutations:
                    all_permutations.append((perm1, perm2, perm3))

        return all_permutations

    def setUnitsOrderingHeuristic(self, heuristic):
        self.unit1.setTasks(heuristic[0])
        self.unit2.setTasks(heuristic[1])
        self.unit3.setTasks(heuristic[2])

        self.units = [self.unit1, self.unit2, self.unit3]
        
        
    def getUnitsOrderingHeuristic(self):
        return [[task.getId() for task in unit.tasks] for unit in self.units]


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

    # Calculate average batchsize


# 8. Printer
# ----------
class Printer:
    def __init__(self):
        self.outputLocation = sys.stdout

    def setOutputFile(self, outputFile):
        self.outputLocation = open(outputFile, "w")

    def removeOutput(self):
        self.outputLocation = None

    def getDocumentWriter(self) -> DocumentWriter.DocumentWriter:
        return self.DocumentWriter

    def createDocument(self, filename, title):
        self.DocumentWriter = DocumentWriter.DocumentWriter(
            "Wafer Production Line - Optimization", "Optimization")
        self.DocumentWriter.save()

    def getBuffers(self, productionLine):
        if self.outputLocation != None:
            for task in productionLine.getTasks():
                print(task.getLoadBuffer().getBatches())
                for batch in task.getLoadBuffer().getBatches():
                    print(
                        f"batch {batch.getId()} in buffer {task.getLoadBuffer().getId()}")
            batch_ids = [batch.getId()
                         for batch in productionLine.buffer10.getBatches()]
            print(f"Ids of batches in last buffer: {batch_ids}")

    def getTasks(self, productionLine, outputLocation):
        if self.outputLocation != None:
            for task in productionLine.getTasks():
                print(task.getCurrentlyProcessingBatch())

    def printEventQueue(self, eventQueue, outputLocation):
        if self.outputLocation != None:
            outputLocation.write("Waiting Events\n")
            for event in eventQueue.getEventQueue():
                self.printEvent(event, outputLocation)

    def printTasks(self,productionline,outputLocation):
        for task in productionline.getTasks():
            outputLocation.write(f"Task {task.getId()} with loadingbuffer {task.getLoadingBuffer()} and unloadingbuffer {task.getUnloadingBuffer()}\n")

    def printUnits(self,productionline,outputLocation):
        for unit in productionline.getUnits():
            outputLocation.write(f"Unit {unit.getId()} with tasks: {unit.getTasks()}\n")

    def printEvent(self, event, outputLocation):
        if self.outputLocation != None:
            outputLocation.write(
                f"Event: {event.getEventAction()} at {event.getEventTime()} on unit {event.getEventUnit().getId()}\n")

    def printIntroduction(self, simulation, outputLocation):
        if self.outputLocation != None:
            outputLocation.write(
                f"\nHere is a simulation of {len(simulation.getBatches())} Batches running`\n")
            average = simulation.getAverageBatchSize()
            outputLocation.write(
                f"The batches are produced randomly and have an average size of {round(average,1)}\n")
            outputLocation.write(f"The total runTime is found at the bottom\n\n")

    def printLoadedToSim(self, batch, event, outputLocation):
        if self.outputLocation != None:
            outputLocation.write(
                f"Loaded batch {batch.getId()} with size {batch.getBatchSize()} to simulation at time {event.getEventTime()}\n")

    def printLoad(self, batch, task, event, outputLocation):
        if self.outputLocation != None:
            outputLocation.write(
                f"Loaded batch {batch.getId()} to task {task.getId()} at time {event.getEventTime()}\n")

    def printUnload(self, batch, task, event, outputFile):
        if self.outputLocation != None:
            outputFile.write(
                f"Unloaded batch {batch.getId()} from task {task.getId()} at time {event.getEventTime()}\n")

    def printTotal(self, simulation, outputFile):
        if self.outputLocation != None:
            outputFile.write(
                f"\n\nTotal runtime was {simulation.getCurrentTime()}")


# 9. Simulation
# -------------
class Simulation:

    def __init__(self, wafersToProduce) -> None:
        self.wafersToProduce = wafersToProduce
        self.eventqueue = []
        self.batches = []
        self.currentTime = 0
        self.productionLine = ProductionLine()
        self.units = self.productionLine.getUnits()
        self.printer = Printer()
        self.batchSize = None
        self.interval = 0
        self.timebetween = 60

    def getEventQueue(self):
        return self.eventqueue

    # Calculate average batch size
    def getAverageBatchSize(self):
        tot = 0
        for batch in self.batches:
            tot += batch.getBatchSize()
        return tot / len(self.batches)

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
        heapq.heappush(self.getEventQueue(), event)

    def getTimeBetweenBatches(self):
        return self.timebetween

    def setTimeBetweenBatches(self, time):
        self.timebetween = time

    def getInterval(self):
        return self.interval

    def setInterval(self, interval):
        self.interval = interval

    def createBatches(self):
        index = 0

        while self.wafersToProduce > 0:
            batch = Batch(index+1, self.getBatchSize())
            self.wafersToProduce -= batch.getBatchSize()
            self.addBatches(batch)
            heapq.heappush(self.eventqueue, Event(
                self.timebetween, "loadBatchToSimulation", self.productionLine.getUnits()[0]))
            self.timebetween += self.interval
            index += 1

    def runSimulation(self):
        unit1 = self.productionLine.getUnits()[0]
        unit2 = self.productionLine.getUnits()[1]
        unit3 = self.productionLine.getUnits()[2]
        for task in unit1.getTasks():
            if task.getId() == 1:
                task1 = task

        self.printer.printIntroduction(self, self.printer.outputLocation)

        while self.getEventQueue():
            self.setCurrentTime(self.getFirst().getEventTime())
            currentEvent = heapq.heappop(self.eventqueue)

            currentUnit = currentEvent.getEventUnit()
            if currentUnit == None:
                continue
            # load batches to simulation
            # --------------------------
            if currentEvent.getEventAction() == "loadBatchToSimulation":
                if (len(self.batches) == 0):
                    continue
                elif task1.getLoadBuffer().canInsertBatch(self.batches[0]):
                    batch = self.batches.pop(0)
                    task1.getLoadBuffer().insertBatch(batch)
                    heapq.heappush(self.getEventQueue(), Event(
                        self.getCurrentTime() + 1, "load", unit1))
                    self.printer.printLoadedToSim(
                        batch, currentEvent, self.printer.outputLocation)
                else:
                    heapq.heappush(self.getEventQueue(), Event(
                        self.getCurrentTime()+1, "loadBatchToSimulation", unit1))

            # load batches to a task
            # --------------------------
            elif currentEvent.action == "load":
                for task in currentUnit.getTasks():
                    # print(task.getId(), "Her er IDEN!")
                    bool, batch = currentUnit.canProcessBatch(task)
                    if bool:
                        time = task.processBatch(batch) 
                        currentUnit.setCurrentlyProcessingTask(task)
                        currentUnit.getCurrentlyProcessingTask().setCurrentlyProcessingBatch(batch)
                        heapq.heappush(self.getEventQueue(), Event(
                            self.getCurrentTime() + time + 1, "unload", currentUnit))
                        self.printer.printLoad(
                            batch, task, currentEvent, self.printer.outputLocation)
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
                    self.currentTime + 1, "load", currentUnit))
                self.printer.printUnload(
                    batch, currentTask, currentEvent, self.printer.outputLocation)
                # Siste Task på unit 1
                if self.productionLine.getUnitFromTask(nextTask) == None:
                    if len(self.getEventQueue()) == 0:
                        continue
                    heapq.heappush(self.eventqueue, Event(
                        self.currentTime + 1, "load", unit2))
                    heapq.heappush(self.eventqueue, Event(
                        self.currentTime + 1, "load", unit3))
                else:
                    heapq.heappush(self.eventqueue, Event(
                        self.currentTime + 1, "load", self.productionLine.getUnitFromTask(nextTask)))

        self.printer.printTotal(self, self.printer.outputLocation)
        print("Simulation finished", self.currentTime)


# 10. Optimization
def worstCase():
    # Manual to send in one batch at a time
    wafersToProduce = 1000
    index = 0
    totalTime = 0
    # Creating one batch then run the simulation
    while wafersToProduce > 0:
        batch = Batch(index, None)
        simulation = Simulation(batch.getBatchSize())
        wafersToProduce -= batch.getBatchSize()
        index += 1
        simulation.createBatches()
        simulation.runSimulation()
        totalTime += simulation.getCurrentTime()
    return totalTime


def reducingTimeBetweenBatches():
    numberOfSimulations = 130  # This number changes time between batches
    sim1 = [[], []]  # time and time between batches
    sim2 = [[], []]  # time and time between batches
    sim3 = [[], [], []]  # time, time between batches and average batchsize
    while numberOfSimulations > 50:
        simulation1 = Simulation(1000)
        simulation2 = Simulation(1)
        simulation3 = Simulation(1)

        # Simulation 1 with batchsize 20
        simulation1.setBatchSize(20)
        # Removes the print that runs every simulation
        simulation1.getPrinter().removeOutput()
        # Increase time between loading with a constant number
        simulation1.setInterval(numberOfSimulations)
        # Change the loading time between batches to be the same number as simulations
        simulation1.setTimeBetweenBatches(0)
        simulation1.createBatches()
        simulation1.runSimulation()
        sim1[0].append(simulation1.getCurrentTime())
        sim1[1].append(numberOfSimulations)

        # Simulation 2 with batchsize 50
        simulation2.setBatchSize(50)
        # Removes the print that runs every simulation
        simulation2.getPrinter().removeOutput()
        # Increase time between loading with a constant number
        simulation2.setInterval(numberOfSimulations)
        # Change the loading time between batches to be the same number as simulations
        simulation2.setTimeBetweenBatches(0)
        simulation2.createBatches()
        simulation2.runSimulation()
        sim2[0].append(simulation2.getCurrentTime())
        sim2[1].append(numberOfSimulations)

        simulation3.setBatchSize(None)
        # Removes the print that runs every simulation
        simulation3.getPrinter().removeOutput()
        # Increase time between loading with a constant number
        simulation3.setInterval(numberOfSimulations)
        # Change the loading time between batches to be the same number as simulations
        simulation3.setTimeBetweenBatches(0)
        simulation3.createBatches()
        # sim3[2].append(simulation3.getAverageBatchSize())
        # print(simulation3.getAverageBatchSize())
        simulation3.runSimulation()
        sim3[0].append(simulation3.getCurrentTime())
        sim3[1].append(numberOfSimulations)
        del simulation1
        del simulation2
        del simulation3

        numberOfSimulations -= 1
    #print(sim1[0])
    #print(sim1[1])
    figure("figure_batchSize_20", "Time", "Loading time between batches",
           sim1, xlim=(50, 125), ylim=(5500, 6600), title="Batchsize 20")
    figure("figure_batchSize_50", "Time", "Loading time between batches",
           sim2, xlim=(240, 300), ylim=(5700, 6600), title="Batchsize 50")
    figure("figure_batchSize_50_Whole", "Time", "Loading time between batches",
           sim2, xlim=None, ylim=None, title="Batchsize 50 with whole figure")
    figure("figure_batchSize_Random", "Time", "Loading time between batches",
           sim3, xlim=None, ylim=None, title="Random batchsize per simulation")

    # print(min(sim1[0]))
    # print(min(sim2[0]))
    # print(min(sim3[0]))
    return [sim1, sim2, sim3]


def figure(filename, ylabel, xlabel, data, xlim=None, ylim=None, title=None):
    plt.plot(data[1], data[0])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.title(title)
    plt.savefig(str(filename) + '.png')
    plt.clf()


def changeOrderingHeuristicAndLoadingtimes():
    numberOfSimulations = 112  # This number changes time between batches
    results = []
    sim1 = []  # time and time between batches and permutation
    simulationForPermutaions = Simulation(1)
    task_permutations = simulationForPermutaions.getProductionLine(
    ).generate_task_permutations()
    ###FJERN DENNE ETTERPÅ
    task_permutations = task_permutations[100:200]
    ###FJERN DENNE ETTERPÅ

    while numberOfSimulations > 103:
        
        best_results_sim1 = [[], [], []]
        
        for i, permutation in enumerate(task_permutations):
            simulation1 = Simulation(1000)
            # print(f"Permutation {i + 1}:")
            # print(
            #     f"  Unit 1: {permutation[0][0].getId()}, {permutation[0][1].getId()}, {permutation[0][2].getId()}, {permutation[0][3].getId()}")
            # print(
            #     f"  Unit 2: {permutation[1][0].getId()}, {permutation[1][1].getId()}, {permutation[1][2].getId()}")
            # print(
            #     f"  Unit 3: {permutation[2][0].getId()}, {permutation[2][1].getId()}\n")
            simulation1.getProductionLine().setUnitsOrderingHeuristic(permutation)

            # Simulation 1 with batchsize 20
            simulation1.setBatchSize(20)
            # Removes the print that runs every simulation
            simulation1.getPrinter().removeOutput()
            # Increase time between loading with a constant number
            simulation1.setInterval(numberOfSimulations)
            # Change the loading time between batches to be the same number as simulations
            simulation1.setTimeBetweenBatches(0)
            simulation1.createBatches()
            simulation1.runSimulation()
            best_results_sim1[0].append(simulation1.getCurrentTime())
            best_results_sim1[1].append(numberOfSimulations)
            best_results_sim1[2].append(permutation)

            # Simulation 2 with batchsize 50

            del simulation1
          
        #Time to find the best result for each simulation
        bestTime_sim1 = min(best_results_sim1[0])
        #Find where in the simulation that happens
        best_sim1 = [bestTime_sim1, best_results_sim1[1][best_results_sim1[0].index(bestTime_sim1)], best_results_sim1[2][best_results_sim1[0].index(bestTime_sim1)]]
        
        #Add the best permutation to the list
        sim1.append(best_sim1)

        
        numberOfSimulations -= 1
        
    allTimeBest1 = min(sim1)

    # print("\n\nresults of sim1", sim1)
    # print("\n\nresults of sim2", sim2)
    # print("\n\nresults of sim3", sim3)
    # print("All time best\n\n", allTimeBest1)
    # print("All time best\n\n",allTimeBest2)
    # print("All time best\n\n",allTimeBest3)
    
    return allTimeBest1
    
    
def changeOrderingHeuristicAndLoadingtimesAndBatchsize(batchsize):
    numberOfSimulations = 1  # This number changes time between batches
    sim1 = []  # time and time between batches and permutation
    simulationForPermutaions = Simulation(1)
    task_permutations = simulationForPermutaions.getProductionLine(
    ).generate_task_permutations()
    
    ###FJERN DENNE ETTERPÅ
    #task_permutations = task_permutations[100:105]
    ###FJERN DENNE ETTERPÅ

    while numberOfSimulations > 0:
        
        
        best_results_sim1 = [[], [], []]
        #Permutations is a list of 288 permutation
        for i, permutation in enumerate(task_permutations):
            simulation1 = Simulation(1000)
            # print(f"Permutation {i + 1}:")
            # print(
            #     f"  Unit 1: {permutation[0][0].getId()}, {permutation[0][1].getId()}, {permutation[0][2].getId()}, {permutation[0][3].getId()}")
            # print(
            #     f"  Unit 2: {permutation[1][0].getId()}, {permutation[1][1].getId()}, {permutation[1][2].getId()}")
            # print(
            #     f"  Unit 3: {permutation[2][0].getId()}, {permutation[2][1].getId()}\n")
            simulation1.getProductionLine().setUnitsOrderingHeuristic(permutation)
            # Simulation 1 with batchsize 20
            simulation1.setBatchSize(batchsize)
            # Removes the print that runs every simulation
            simulation1.getPrinter().removeOutput()
            # Increase time between loading with a constant number
            simulation1.setInterval(numberOfSimulations)
            # Change the loading time between batches to be the same number as simulations
            simulation1.setTimeBetweenBatches(0)
            simulation1.createBatches()
            simulation1.runSimulation()
            best_results_sim1[0].append(simulation1.getCurrentTime())
            best_results_sim1[1].append(numberOfSimulations)
            best_results_sim1[2].append(permutation)
            del simulation1

            
          
        #Time to find the best result for each simulation
        bestTime_sim1 = min(best_results_sim1[0])
       
        #Find where in the simulation that happens
        best_sim1 = [bestTime_sim1, best_results_sim1[1][best_results_sim1[0].index(bestTime_sim1)], best_results_sim1[2][best_results_sim1[0].index(bestTime_sim1)]]
       
        #Add the best permutation to the list
        sim1.append(best_sim1)
        
        numberOfSimulations -= 1
        
    allTimeBest1 = min(sim1)
    #print("\n\nresults of sim1", sim1)
    
    #print("All time best\n\n", allTimeBest1)
    
    
    return allTimeBest1 


#changeOrderingHeuristicAndLoadingtimes()


def task_4_OneBatch():
    sim = Simulation(20)
    sim.getPrinter().setOutputFile("OneBatch.txt")
    sim.createBatches()
    sim.runSimulation()


def task_4_FewBatches():
    sim = Simulation(150)
    sim.getPrinter().setOutputFile("FewBatches.txt")
    sim.createBatches()
    sim.runSimulation()


def task_4_AllBatches():

    sim = Simulation(1000)
    sim.getPrinter().setOutputFile("AllBatches.txt")
    sim.createBatches()
    sim.runSimulation()

def task_4():
    task_4_OneBatch()
    task_4_FewBatches()
    task_4_AllBatches()
    
    

def task_5():
    # Worst Case
    return worstCase(), reducingTimeBetweenBatches()


def task_6():
    # Change ordering heuristic
    return changeOrderingHeuristicAndLoadingtimes()
    
def task_7():
    
    results = []
    
    for batchsize in range(20, 51):
        results.append(changeOrderingHeuristicAndLoadingtimesAndBatchsize(batchsize))
        
    allTimeBest = min(results)
    batchsize = results.index(allTimeBest) + 20
    #print("\nAll time best ", allTimeBest)
    #print("Batchsize ", batchsize)
    #print("Length of results ", len(results))
    batchsizesFigure = [i for i in range(20, 51)]
    #print(batchsizesFigure)
    #print("\n\n Results: ", results)
    first_elements = [sublist[0] for sublist in results]
    #print("First elements" ,first_elements)
    figureList = [first_elements, batchsizesFigure]
    #print("FigureData ", figureList)
    figure("allTimeBest", "Time" , "Batchsize", figureList, title="All time best")
    #Results contains the optimal ordering heuristic for each batchsize
    return results, allTimeBest, batchsize



def optimization():
    st = time.time()
    printer = Printer()
    printer.createDocument(
        "Wafer Production Line - Optimization", "Optimization")

    worstCaseTime, simulations = task_5()
    printer.getDocumentWriter().addSection()
    printer.getDocumentWriter().addHeading("2.3 Optimization", 1)
    printer.getDocumentWriter().addHeading("Task 5.", 1)
    printer.getDocumentWriter().addHeading("Simulation with Worst Case", 2)
    printer.getDocumentWriter().addParagraph("This is an example of runtime with the worst case solution. One batch is loaded into the simulation, and the next one is not loaded until the first one is finished. This is repeated until all 1000 wafers is produced. The batch sizes is random from 20 to 50 wafers per batch, and therefore some variation in time between each run. The total runtime is: " + str(worstCaseTime) + " minutes for this simulation.")

   # Current optimization with reduced loading times
    printer.getDocumentWriter().addHeading(
        "Simulation with reduced loadtime between batches", 2)
    printer.getDocumentWriter().addParagraph("Now we will try to reduce the loading time between the batches. We will simulate 3 simulations, with batch sizes of 20, 50 and random batch size. The graphs below will show the loading times, and the finish time for all 1000 Wafers. The loading time between each batch is increased with a constant number, and the loading time between each batch is the same as the number of simulations. The loading time between each batch is increased from 1 to 300 minutes.")
    printer.getDocumentWriter().addPicture("figure_batchSize_20.png", 6)
    printer.getDocumentWriter().addParagraph("Batchsize 20: The optimal solution is with total time: " +
                                             str(min(simulations[0][0])) + " and loading time between batches " + str(simulations[0][1][simulations[0][0].index(min(simulations[0][0]))]) + " minutes.")
    printer.getDocumentWriter().addPicture("figure_batchSize_50.png", 6)
    printer.getDocumentWriter().addParagraph("Batchsize 50: The optimal solution is with total time: " +
                                             str(min(simulations[1][0])) + " and loading time between batches " + str(simulations[1][1][simulations[1][0].index(min(simulations[1][0]))]) + " minutes.")
    printer.getDocumentWriter().addPicture("figure_batchSize_50_Whole.png", 6)
    printer.getDocumentWriter().addParagraph(
        "Observe that the optimal loading time between each task from batchsize 20 and batchsize 50 is proportional to the batchsize.")
    printer.getDocumentWriter().addPicture("figure_batchSize_Random.png", 6)
    printer.getDocumentWriter().addParagraph("Batchsize 20: The optimal solution is with total time: " + str(min(simulations[2][0])) + " and loading time between batches " + str(
        simulations[2][1][simulations[2][0].index(min(simulations[2][0]))]) + " minutes. NOTE: With random batchsize, the optimal solution is likely to change from run to run.")
    
    printer.getDocumentWriter().addSection()
    printer.getDocumentWriter().addHeading("Task 6.", 1)
    printer.getDocumentWriter().addHeading("Simulation with changed ordering heuristic", 2)
    printer.getDocumentWriter().addParagraph("The previous results show the optimal time with 20, 50 and random batch sizes with standard task prioritization, with Unit 1 : [1, 3, 6, 9], Unit 2 : [2, 5, 7] and Unit 3 : [4, 8]. Now we will change the order tasks are prioritized. It is 288 possible permutations of the tasks, and we will simulate the 3 same simulations. That means 300 simulations, with different load time, times 288 permutations. The total number of simulations is 86 400 per batch size. The results are shown below.")
    allTimeBest1 = task_6()
    printer.getDocumentWriter().addParagraph("The best solution for batchsize 20 is with total time: " + str(allTimeBest1[0]) + " and loading time between batches " + str(allTimeBest1[1]) + " minutes." + " and the best ordering heuristic is: Unit 1 : [" + ", ".join([str(task.getId()) for task in allTimeBest1[2][0]]) + "] Unit 2: [" + ", ".join([str(task.getId()) for task in allTimeBest1[2][1]]) + "] Unit 3: [" + ", ".join([str(task.getId()) for task in allTimeBest1[2][2]]) + "]" )
    # results, allTimeBest, batchSize = task_7()
    # printer.getDocumentWriter().addSection()
    # printer.getDocumentWriter().addHeading("Task 7.", 1)
    # printer.getDocumentWriter().addHeading("Simulation with different loading time, ordering heuristic and batchsizes", 2)
    # printer.getDocumentWriter().addParagraph("Now we will simulate the same as in task 6, but with different batch sizes for each simulation. That means that we will run 288 permutations * (50-20) batch sizes * 300 loading times = 2 592 000 simulations! We will only show the best times for each batch size, but the best loading time and ordering heuristic for the best time overall with all optimization. This is probably an overkill solution, but will give us the best results and overview into the problem at hand.")
    # printer.getDocumentWriter().addParagraph("The all time best solution is with total time: " + str((allTimeBest[0])) + " and loading time between batches " + str(allTimeBest[1]) + " minutes. The optimal batch size is then " + str(batchSize) + " wafers per batch, " + " and the best ordering heuristic is: Unit 1 : [" + ", ".join([str(task.getId()) for task in allTimeBest[2][0]]) + "] Unit 2: [" + ", ".join([str(task.getId()) for task in allTimeBest[2][1]]) + "] Unit 3: [" + ", ".join([str(task.getId()) for task in allTimeBest[2][2]]) + "]")
    # printer.getDocumentWriter().addParagraph("\n\nThe figure below shows the optimal time for each batch size, with the most optimal loading time and ordering heuristic. NOTE: The optimal solution is likely to change from run to run since the simulations is run with random batchsizes each time.")
    # printer.getDocumentWriter().addPicture("allTimeBest.png", 6)
    et = time.time()
    elapsed_time = round(et - st, 2)
    print('Execution time:', elapsed_time, 'seconds')
    printer.getDocumentWriter().addParagraph("Execution time for the whole optimization process: " + str(elapsed_time) + " seconds, ran with a good computer")
    
#optimization()
st = time.time()

allTimeBest1 = changeOrderingHeuristicAndLoadingtimes()
print("The best solution for batchsize 20 is with total time: " + str(allTimeBest1[0]) + " and loading time between batches " + str(allTimeBest1[1]) + " minutes." + " and the best ordering heuristic is: Unit 1 : [" + ", ".join([str(task.getId()) for task in allTimeBest1[2][0]]) + "] Unit 2: [" + ", ".join([str(task.getId()) for task in allTimeBest1[2][1]]) + "] Unit 3: [" + ", ".join([str(task.getId()) for task in allTimeBest1[2][2]]) + "]" )
et = time.time()
elapsed_time = round(et - st, 2)
print('Execution time:', elapsed_time, 'seconds')
# 10. Main
# --------


def main():
    simulation = Simulation(1000)
    perm = (simulation.getProductionLine().generate_task_permutations()[280])
    simulation.getProductionLine().setUnitsOrderingHeuristic(perm)
    print(simulation.getProductionLine().getUnitsOrderingHeuristic())
    # Task_5()
    simulation.createBatches()
    simulation.runSimulation()
    # worstCase()

    # sim.printAllBuffers()

    # sim.printAllBuffers()

#main()

# task_4_AllBatches()
