

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

    def all_batches_finished(self):
        for unit in self.units:
            for task in unit.getTasks():
                for batch in task.getBuffer().getBatches():
                    if batch.getState() != Batches.FINISHED:
                        return False
        return True
    
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