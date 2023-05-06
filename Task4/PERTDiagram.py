import Printer,sys,random
import pandas as pd
import Task
#import pygraphviz as pgv
from IPython.display import Image



class PERTdiagram:

    def __init__(self):

        self.criticalPath = []
        self.tasks = []
        self.shortestduration = 0
        self.modeduration = 0
        self.longestduration = 0
        self.riskfactor = 0
        self.actualduration = 0
        self.earlyCompletionDates = []
        self.intermediategate = 0
        self.printer = Printer.Printer(sys.stdout)

    # Finds the Critical Path
    def findCriticalPath(self):
        self.getCriticalPath().clear()
        for task in self.getTasks():
            task.setSlack(task.LS - task.ES)
            if task.getSlack() == 0:
                task.setCritical(True)
                self.getCriticalPath().append(task)
            else:
                task.setCritical(False)

    def getCriticalPath(self):
        return self.criticalPath

    def setTasks(self, tasks):
        self.tasks = tasks

    def getTasks(self):
        return self.tasks

    def addTask(self, task):
        self.getTasks().append(task)

    def removeTask(self, task):
        self.tasks.remove(task)

    def setShortestDuration(self, duration):
        self.shortestduration = duration

    def getShortestDuration(self):
        return self.shortestduration

    def setModeDuration(self, duration):
        self.modeduration = duration

    def getModeDuration(self):
        return self.modeduration

    def setLongestDuration(self, duration):
        self.longestduration = duration

    def getLongestDuration(self):
        return self.longestduration

    def setRiskfactor(self):
        rf = random.choice([0.8, 1.0, 1.2, 1.4])
        for task in self.tasks:
            task.riskfactor = rf
        self.riskfactor = rf

    def getRiskFactor(self):
        return self.riskfactor

    def setActualDuration(self, duration):
        self.actualduration = duration

    def getActualDuration(self):
        return self.actualduration

    def setEarlyCompletionDates(self):
        self.earlyCompletionDates = []
        for task in self.tasks:
            self.earlyCompletionDates.append(task.EF)

    def getEarlyCompletionDates(self):
        return self.earlyCompletionDates

    def getIntermediateGate(self):
        return self.intermediategate

    def setIntermediateGate(self, index):
        self.intermediategate = index

    # Methods

    def get_description_column_name(self, df):
        if 'Description' in df.columns:
            return 'Description'
        elif 'Descriptions' in df.columns:
            return 'Descriptions'
        else:
            raise ValueError(
                "No 'Description' or 'Descriptions' column found in the DataFrame")

    def collectProjectFromExcel(self, excelFile, sheetname):
        df = pd.read_excel(excelFile, sheetname, header=0, index_col=None)
        description_column = self.get_description_column_name(df)

        for index, row in df.iterrows():
            if row.isnull().all():
                continue
            id = row['Codes']
            description = row[description_column] if row[description_column] else 'nan'
            duration = [int(d) for d in row['Durations'].strip('()').split(
                ',')] if not isinstance(row['Durations'], float) else [0, 0, 0]
            cleaned_duration = [int(str(dur).strip(" ")) for dur in duration]
            predecessors = row['Predecessors'].split(
                ', ') if not isinstance(row['Predecessors'], float) else []
            if description and duration:
                task = Task.Task(id, description, cleaned_duration,
                                 [], self.getRiskFactor())
            else:
                task = Task.Task(id, '', [0, 0, 0], [], self.getRiskFactor())
            self.addTask(task)

        # Now that all tasks have been created, establish the connections between tasks based on predecessors
        for index, row in df.iterrows():
            if index < 1:
                continue
            task_id = row['Codes']
            predecessors = row['Predecessors'].split(
                ', ') if not isinstance(row['Predecessors'], float) else []
            for predecessor_id in predecessors:
                if predecessor_id:  # Avoid empty predecessor strings
                    self.connect_tasks(predecessor_id, task_id)

    def connect_tasks(self, predecessor, successor):
        predecessor_task = self.find_task_by_id(predecessor)
        successor_task = self.find_task_by_id(successor)
        if predecessor_task and successor_task:
            predecessor_task.addSuccessor(successor_task)
            successor_task.addPredecessor(predecessor_task)

    def disconnect_tasks(self, predecessor, successor):
        predecessor_task = self.find_task_by_id(predecessor)
        successor_task = self.find_task_by_id(successor)

        if predecessor_task and successor_task:
            predecessor_task.removeSuccessor(successor_task)
            successor_task.removePredecessor(predecessor_task)

    def find_task_by_id(self, task_id):
        for task in self.getTasks():
            if task.getId() == task_id:
                return task
        return None

    def calculateDurations(self):
        for task in self.getTasks():
            task.setDuration(task.getMin())
        self.calculate()
        self.setShortestDuration(self.find_task_by_id('Completion').getLF(
        ) if self.find_task_by_id('Completion') else self.find_task_by_id('End').getLF())
        for task in self.tasks:
            task.setDuration(task.getMode())
        self.calculate()
        self.setModeDuration(self.find_task_by_id('Completion').getLF(
        ) if self.find_task_by_id('Completion') else self.find_task_by_id('End').getLF())
        for task in self.tasks:
            task.setDuration(task.getMax())
        self.calculate()
        self.setLongestDuration(self.find_task_by_id('Completion').getLF(
        ) if self.find_task_by_id('Completion') else self.find_task_by_id('End').getLF())
        self.calculatActualDuration()
        self.setEarlyCompletionDates()
        # self.printer.print_all_tasks(self.getTasks())
        #self.printer.printDurations(self)

    def calculatActualDuration(self):
        self.setRiskfactor()
        for task in self.getTasks():
            task.setNewmode()
        self.calculate()
        self.setActualDuration(self.find_task_by_id('Completion').getLF(
        ) if self.find_task_by_id('Completion') else self.find_task_by_id('End').getLF())

    def calculate(self):
        self.forwardPass()
        self.backwardPass()
        self.findCriticalPath()

    def forwardPass(self):
        for task in self.getTasks():
            if task.getId() == 'Start':
                continue
            if task.getPredecessors() == ['Start']:
                task.setES(0)
                task.setEF(task.getDuration())
            else:
                task.setES(max([t.getEF() for t in task.getPredecessors()]))
                task.setEF(round(task.getES() + task.getDuration()))

    def backwardPass(self):
        for task in reversed(self.tasks):
            if len(task.successors) == 0:
                task.setLF(task.getEF())
                task.setLS(round(task.getLF() - task.getDuration()))
            else:
                task.setLF(min([t.getLS() for t in task.getSuccessors()]))
                task.setLS(round(task.getLF() - task.getDuration()))

    def classifyProject(self):
        if self.getActualDuration() <= self.getModeDuration() * 1.05:
            self.category = "Successful"
        elif self.getModeDuration() * 1.05 < self.getActualDuration() <= self.getModeDuration() * 1.15:
            self.category = "Acceptable"
        else:
            self.category = "Failed"
        return self.category

    def createAndVisualizeGraphWithDepth(self, filename):
        return
        #The code below is used to create all the images for the PERT Diagram.
        #
        A = pgv.AGraph(directed=True, strict=True, ranksep='1.5', rankdir='LR')

        #add nodes
        for task in self.tasks:
            if task == self.getTasks()[self.getIntermediateGate()]:
                A.add_node(task.getId(), label=task.getId() + 'Gate', shape='circle',
                           style='filled', fillcolor='red')
            else:
                A.add_node(task.getId(), label=task.getId(), shape='circle',
                        style='filled', fillcolor='skyblue')

        # Add edges
        for task in self.getTasks():
            for predecessor in task.getPredecessors():
                A.add_edge(predecessor.getId(), task.getId())

        # Draw the graph
        A.layout(prog='dot')
        A.draw(filename)

        # Display the graph
        
        return Image(filename=filename)