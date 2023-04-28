import random
import sys


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
        self.startProcessingTime = -1
        self.finishedTime = -1
        self.tasksFinished = []

    def getIdentifier(self):
        return self.identifier

    def addTask(self, task):
        self.tasksFinished.append(task)

    def getTasksFinished(self):
        return self.tasksFinished

    def getBatchSize(self):
        return self.size

    def getState(self):
        return self.state

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

    def getStartProcessingTime(self):
        return self.startProcessingTime

    def setStartProcessingTime(self, time):
        self.startProcessingTime = time

    def getCompleteProcessingTime(self):
        return self.finishedTime

    def setCompleteProcessingTime(self, time):
        self.finishedTime = time


class Buffer:
    LOADING_TIME = 60
    UNLOADING_TIME = 60

    def __init__(self) -> None:
        self.capacity = 120
        self.batches = []

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
        self.batches.append(batch)

    def removeBatch(self, batch):
        self.batches.remove(batch)

    def popBatch(self):
        return self.batches.pop(0)


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

    def __init__(self, task) -> None:
        self.task = task
        self.processTime = 0
        self.input_buffer = Buffer()
        self.currentlyProcessing = None

    def getTask(self):
        return self.task

    def getProcessTime(self):
        return self.processTime

    def calculateProcessTime(self, batch):
        self.processTime = self.task * batch.getBatchSize()
        return self.processTime

    def processBatch(self, time):
        if self.input_buffer.getBatchSize() > 0:
            self.currentlyProcessing = self.input_buffer.popBatch()
            self.currentlyProcessing.setState(Batches.PROCESSING)
            self.currentlyProcessing.setStartProcessingTime(time)
            self.calculateProcessTime(self.currentlyProcessing)
            return self.currentlyProcessing

    def getCurrentlyProcessing(self):
        return self.currentlyProcessing


class Unit:
    def __init__(self, identifier, tasks) -> None:
        self.identifier = identifier
        self.tasks = [Task(task) for task in tasks]
        self.currentlyProcessingTask = None


class ProductionLine:
    def __init__(self) -> None:
        self.units = [Unit("Unit 1", [Task.TASK_1, Task.TASK_3, Task.TASK_6, Task.TASK_9]), Unit(
            "Unit 2", [Task.TASK_2, Task.TASK_5, Task.TASK_7]), Unit("Unit 3", [Task.TASK_4, Task.TASK_8])]
        self.input_buffer = Buffer()
        self.task_order = [Task.TASK_1, Task.TASK_2, Task.TASK_3, Task.TASK_4,
                           Task.TASK_5, Task.TASK_6, Task.TASK_7, Task.TASK_8, Task.TASK_9]

    def getUnits(self):
        return self.units

    def findTaskByIdentifier(self, identifier):
        for unit in self.units:
            for task in unit.tasks:
                if task.getTask() == identifier:
                    return task
        return None

    def loadBatchToTask(self, batch, task_type):
        task = self.findTaskByIdentifier(task_type)
        if task is None:
            raise Exception(f"Task type {task_type} not found")
        task.input_buffer.insertBatch(batch)

    def unloadBatchFromTask(self, taskIdentifier):
        task = self.findTaskByIdentifier(taskIdentifier)
        if task is None:
            raise Exception("Task not found")
        batch = task.input_buffer.popBatch()
        return batch

    def processBatches(self):
        currentTime = 0
        totalWafers = 0
        task_order_idx = 0

        while totalWafers < 1000:
            current_task = self.task_order[task_order_idx]
            task = self.findTaskByIdentifier(current_task)

            if len(self.input_buffer.getBatches()) > 0 and task_order_idx == 0:
                batch = self.input_buffer.popBatch()
                task.input_buffer.insertBatch(batch)

            if task.currentlyProcessing is None:
                batch = task.processBatch(currentTime)
                if batch:
                    print(
                        f"Processing Batch {batch.getIdentifier()} in Task {task.getTask()}")
                    batch.addTask(task.getTask())

            elif currentTime >= task.currentlyProcessing.getStartProcessingTime() + task.getProcessTime():
                finishedBatch = task.currentlyProcessing
                finishedBatch.setCompleteProcessingTime(currentTime)
                finishedBatch.setState(Batches.FINISHED)
                task.currentlyProcessing = None

                if task_order_idx == len(self.task_order) - 1:
                    totalWafers += finishedBatch.getBatchSize()
                    print(
                        f"Batch {finishedBatch.getIdentifier()} completed at time {currentTime} with {totalWafers} wafers produced and it followed this order: {finishedBatch.getTasksFinished()}")
                else:
                    next_task = self.task_order[task_order_idx + 1]
                    self.loadBatchToTask(finishedBatch, next_task)

            task_order_idx = (task_order_idx + 1) % len(self.task_order)
            currentTime += 1
        print(f"Total wafers produced: {totalWafers}")


def main():
    production_line = ProductionLine()

    batch_identifier = 1
    while production_line.input_buffer.getBatchSize() < 120:
        batch = Batches(batch_identifier)
        batch.setArrivalTime(0)
        batch.setState(Batches.WAITING)
        production_line.input_buffer.insertBatch(batch)
        batch_identifier += 1

    production_line.processBatches()


if __name__ == "__main__":
    main()
