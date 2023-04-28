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

# 2. Batches
# -----------


class Batches:
    NONE = 0
    WAITING = 1
    PROCESSING = 2
    FINISHED = 3

    def __init__(self, identifier) -> None:
        self.identifier = identifier
        self.size = random.randint(20, 50)
        self.state = Batches.NONE
        self.arrivalTime = -1
        self.ProcessingTime = -1
        self.finishedTime = -1
        self.taskRemaining = list(range(1, 10))

    def getIdentifier(self):
        return self.identifier

    def getBatchSize(self):
        return self.size

    def getState(self):
        return self.state

    def getTasksRemaining(self):
        return self.taskRemaining

    def getNextTask(self):
        return self.taskRemaining[0]

    def removeDoneTask(self):
        self.taskRemaining.remove(self.getNextTask())

    def setState(self, state):
        self.state = state

    def serializeState(self):
        if self.state == Batches.NONE:
            return "None"
        elif self.state == Batches.WAITING:
            return "waiting"
        elif self.state == Batches.PROCESSING:
            return "processing"
        elif self.state == Batches.FINISHED:
            return "finished"
        else:
            return "???"

    def getArrivalTime(self):
        return self.arrivalTime

    def setArrivalTime(self, time):
        self.arrivalTime = time

    def getProcessingTime(self):
        return self.ProcessingTime

    def setProcessingTime(self, time):
        self.ProcessingTime = time

    def addProcessingTime(self, time):
        self.ProcessingTime += time

    def getCompleteProcessingTime(self):
        return self.finishedTime

    def setCompleteProcessingTime(self, time):
        self.finishedTime = time

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

    def getBatchSize(self):
        size = 0
        for batch in self.batches:
            size += batch.getBatchSize()
        return size

    def insertBatch(self, batch):
        if self.getBatchSize() + batch.getBatchSize() > self.capacity:
            print("Not enough space in buffer")
            return
        self.batches.append(batch)
    def canInsertBatch(self, batch):
        if self.getBatchSize() + batch.getBatchSize() > self.capacity:
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
        self.processTime = (self.task * batch.getBatchSize()) + Buffer.LOADING_TIME + Buffer.UNLOADING_TIME
        return self.processTime
    
    def get_individual_processing_times(self):
        processing_times = []
        for batch in self.input_buffer.getBatches():
            remaining_time = self.calculateProcessTime(batch) 
            processing_times.append(remaining_time)
        
        return processing_times

    def getNextBufferCapacity(self, Task):
        return Task.getBuffer().getCapacity()

    # Ikke helt ferdig enda, burde sjekke neste batch sin størrelse og se om den passer i bufferen
    def canProsessBatch(self):
        nextBufferCap = self.nextTask.getBuffer().getCapacity(
        ) if self.nextTask != None else sys.maxsize
        # Sjekker først om det er noe å produsere
        if self.input_buffer.getBatchSize() > 0 and self.currentlyProcessing == None:
            for batch in self.input_buffer.getBatches():
                # Sjekker om det er plass i noen av batchene
                if batch.getBatchSize() <= nextBufferCap and batch.getNextTask() == self.getTasknr():
                    return True, batch
        return False, None

    def processBatch(self, batch, nextTask):
        # Kan da produsere batchen, og flytte den videre
        print(
            f"Processing batch {batch.getIdentifier()} in task {self.getTasknr()}")
        self.currentlyProcessing = self.input_buffer.removeAndGetBatch(batch)
        self.currentlyProcessing.removeDoneTask()  # d
        self.currentlyProcessing.addProcessingTime(
            self.getBuffer().LOADING_TIME)
        self.currentlyProcessing.setState(Batches.PROCESSING)
        self.currentlyProcessing.addProcessingTime(
            self.calculateProcessTime(self.currentlyProcessing))

        if len(self.currentlyProcessing.getTasksRemaining()) > 0:
            self.currentlyProcessing.setState(Batches.WAITING)
        else:
            self.currentlyProcessing.setState(Batches.FINISHED)

        self.currentlyProcessing.addProcessingTime(
            self.getBuffer().UNLOADING_TIME)
        if self.taskNr == 9:
            self.output_buffer.insertBatch(self.currentlyProcessing)
        else:
            # Task 9 er siste, så der er buffer ikke til en egen task
            nextTask.getBuffer().insertBatch(self.currentlyProcessing)
        self.currentlyProcessing = None

    def getCurrentlyProcessing(self):
        return self.currentlyProcessing


class Unit:

    def __init__(self, identifier, tasks) -> None:
        self.identifier = identifier
        self.tasks = [Task(task[0], task[1]) for task in tasks]
        self.currentlyProcessingTask = None

    def getIdentifier(self):
        return self.identifier

    def getTasks(self):
        return self.tasks

    def getCurrentlyProcessingTask(self):
        return self.currentlyProcessingTask

    def processTask(self):
        if self.getCurrentlyProcessingTask() == None:
            for task in self.tasks:
                # Går gjennom de første taskene hvis de kan produsere noe
                bool, batch = task.canProsessBatch()
                if bool:
                    self.currentlyProcessingTask = task
                    self.currentlyProcessingTask.processBatch(
                        batch, self.currentlyProcessingTask.getNextTask())
                    print(f"{self.identifier} is processing batch {batch.getIdentifier()}, with task {self.currentlyProcessingTask.getTasknr()} with {batch.getBatchSize()} wafers.")
                    print(
                        f"Tasks remaining for batch {batch.getIdentifier()}: {batch.getTasksRemaining()}")
                    self.currentlyProcessingTask = None
                    return True
        else:
            print("Currently processing task")
        return False

class Event:
    def __init__(self, time, action, unit) -> None:
        self.time = time
        self.action = action
        self.unit = unit
        
        

class TaskScheduler:
    def __init__(self, tasks):
        self.tasks = tasks

    def find_closest_processing_times(self):
        task_processing_times = {}
        for task in self.tasks:
            task_processing_times[task] = task.get_individual_processing_times()

        min_difference = sys.maxsize
        closest_tasks = []

        for task1, times1 in task_processing_times.items():
            for task2, times2 in task_processing_times.items():
                if task1 != task2:
                    for time1 in times1:
                        for time2 in times2:
                            difference = abs(time1 - time2)
                            if difference < min_difference:
                                min_difference = difference
                                closest_tasks = [task1, task2]
        print("Closest tasks: ", closest_tasks)
        
        return closest_tasks

    def get_next_task(self, closest_tasks):
        if closest_tasks:
            return closest_tasks.pop(0)
        return None

class ProductionLine:
    def __init__(self) -> None:
        self.units = [Unit("Unit 1", [[Task.TASK_1, 1], [Task.TASK_3, 3], [Task.TASK_6, 6], [Task.TASK_9, 9]]),
                      Unit("Unit 2", [[Task.TASK_2, 2], [
                          Task.TASK_5, 5], [Task.TASK_7, 7]]),
                      Unit("Unit 3", [[Task.TASK_4, 4], [Task.TASK_8, 8]])]
        self.wafersToProduce = 1000
        self.task_queue = deque([0, 1, 0, 2, 1, 0, 1, 2, 0])
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

    def all_batches_finished(self):
        for unit in self.units:
            for task in unit.getTasks():
                for batch in task.getBuffer().getBatches():
                    if batch.getState() != Batches.FINISHED:
                        return False
        return True

    def produceWafers(self):
        index = 0
        total_wafers_produced = 0
        processRound = 0

        all_tasks = []
        for unit in self.units:
            all_tasks.extend(unit.getTasks())
            # print(str(all_tasks) + "All tasks")

        task_scheduler = TaskScheduler(all_tasks)

        while not self.all_batches_finished() or self.wafersToProduce > 0:
            processed = False
            closest_tasks = task_scheduler.find_closest_processing_times()
            
            print(closest_tasks, "Closest tasks")
            next_task = task_scheduler.get_next_task(closest_tasks)

            if next_task and next_task.processTask():
                unit_identifier = next_task.getTask().getIdentifier()
                print(f"Produced wafer in {unit_identifier}")
                print("\n" + str(processRound))
                processed = True

            processRound += 1
            
            #Fikse slik at denne metoden kjlrer på alle units samtidig
            unit_1, unit_2, unit_3 = self.units[0], self.units[1], self.units[2]

            if not processed and self.wafersToProduce > 0:
                startUnit = self.units[0]
                batch = Batches(index)

                if total_wafers_produced + batch.getBatchSize() > 1000:
                    batch.size = 1000 - total_wafers_produced

                total_wafers_produced += batch.getBatchSize()
                self.wafersToProduce -= batch.getBatchSize()
                if (startUnit.getTasks()[0].getBuffer().canInsertBatch(batch)):
                    startUnit.getTasks()[0].getBuffer().insertBatch(batch)
                    print(
                        f"Produced batch {index} with {batch.getBatchSize()} wafers")
                    index += 1
                else:
                    print("Input buffer full, so couldnt produce new")

        print("All batches finished and total time is: " +
      str(self.units[0].getTasks()[3].output_buffer.getBatches()[0].getProcessingTime()) + " And the total wafers produced is: " + str(self.units[0].getTasks()[3].output_buffer.getBatchSize()))




class Printer:
    def __init__(self):
        self.separator = "\t"
        
        


def main():
    productionLine = ProductionLine()
    productionLine.produceWafers()


main()
