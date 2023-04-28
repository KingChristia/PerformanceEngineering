  # def findTaskByIdentifier(self, identifier):
    #     for unit in self.units:
    #         for task in unit.tasks:
    #             if task.getTask() == identifier:
    #                 return task
    #     return None

    # def loadBatchToTask(self, batch, task_type):
    #     for unit in self.units:
    #         for task in unit.tasks:
    #             if task.getTask() == task_type:
    #                 task.input_buffer.insertBatch(batch)
    #                 return
    #     raise Exception(f"Task type {task_type} not found")

    # def unloadBatchFromTask(self, taskIdentifier):
    #     task = self.findTaskByIdentifier(taskIdentifier)
    #     if task is None:
    #         raise Exception("Task not found")
    #     batch = task.buffer.popBatch()
    #     return batch

    # def loadBatchToUnit(self, batch, unitIdentifier):
    #     for unit in self.units:
    #         if unit.identifier == unitIdentifier:
    #             unit.tasks[0].buffer.insertBatch(batch)
    #             return
    #     raise Exception("Unit not found")

    # def unloadBatchFromUnit(self, unitIdentifier):
    #     for unit in self.units:
    #         if unit.identifier == unitIdentifier:
    #             return unit.tasks[-1].buffer.popBatch()
    #     raise Exception("Unit not found")

    # def moveBatchToNextTask(self, batch, currentUnit, currentTaskIndex):
    #     if currentTaskIndex + 1 < len(currentUnit.tasks):
    #         nextTask = currentUnit.tasks[currentTaskIndex + 1]
    #     else:
    #         nextUnitIndex = self.units.index(currentUnit) + 1
    #         if nextUnitIndex < len(self.units):
    #             nextTask = self.units[nextUnitIndex].tasks[0]
    #         else:
    #             return False

    #     nextTask.input_buffer.insertBatch(batch)
    #     return True

    # def processBatches(self):
    #     currentTime = 0
    #     totalWafers = 0
    #     unit_order_index = 0

    #     while totalWafers < 1000:
    #         current_unit = self.units[self.unit_order[unit_order_index]]
    #         unit_order_index = (unit_order_index + 1) % len(self.unit_order)

    #         # Load the next batch from the input buffer to the first task in the current unit
    #         if len(self.input_buffer.getBatches()) > 0:
    #             first_task = current_unit.tasks[0]
    #             if first_task.currentlyProcessing is None and first_task.input_buffer.getBatchSize() == 0:
    #                 batch = self.input_buffer.popBatch()
    #                 first_task.input_buffer.insertBatch(batch)

    #         # Check each unit and task for processing and moving batches
    #         for unit in self.units:
    #             for taskIndex, task in enumerate(unit.tasks):
    #                 # If the task is not processing a batch, try to process a batch from the input buffer
    #                 if task.currentlyProcessing is None:
    #                     batch = task.processBatch(currentTime)
    #                     if batch:
    #                         print(
    #                             f"Processing Batch {batch.getIdentifier()} in {unit.identifier} Task {task.getTask()}")

    #                 # If the task is processing a batch, check if it's finished
    #                 elif currentTime >= task.currentlyProcessing.getStartProcessingTime() + task.getProcessTime():
    #                     finishedBatch = task.currentlyProcessing
    #                     finishedBatch.setCompleteProcessingTime(currentTime)
    #                     finishedBatch.setState(Batches.FINISHED)
    #                     task.currentlyProcessing = None

    #                     # Try to move the batch to the next task's input buffer
    #                     moved = self.moveBatchToNextTask(
    #                         finishedBatch, unit, taskIndex)
    #                     if moved:
    #                         print(
    #                             f"Moved Batch {finishedBatch.getIdentifier()} from {unit.identifier} Task {taskIndex + 1}")

    #                     # If the batch can't be moved, it's the final task and the batch is finished
    #                     else:
    #                         totalWafers += finishedBatch.getBatchSize()
    #                         print(
    #                             f"Batch {finishedBatch.getIdentifier()} completed at time {currentTime} with {totalWafers} wafers produced")

    #         currentTime += 1



    # productionLine = ProductionLine()
    # i = 0
    # total_wafers = 0

    # while total_wafers < 1000:
    #     batch = Batches(i)
    #     productionLine.loadBatchToTask(batch, Task.TASK_1)
    #     total_wafers += batch.getBatchSize()
    #     print("Batch {} loaded to task 1, with batchSize {}".format(
    #         i, batch.getBatchSize()))
    #     i += 1
    # print(total_wafers)
    # productionLine.processBatches()
