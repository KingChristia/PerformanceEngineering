

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
