

import pandas as pd
import random

class Task:

    def __init__(self,id,description,duration,predecessors):
        self.id = id
        self.description = description

        self.predecessors = predecessors
        self.successors = []

        self.min = duration[0]
        self.mode = duration[1]
        self.max = duration[2]

        self.duration = self.mode #round(random.triangular(self.min,self.max,self.mode),2)

        self.ES = 0
        self.EF = 0
        self.LS = 0
        self.LF = 0
        self.slack = 0

        self.critical = False
        
    def setPredecessors(self, predecessors):
        self.predecessors = predecessors
        
    def add_predecessor(self, predecessor):
        if predecessor not in self.predecessors:
            self.predecessors.append(predecessor)
    
    def setPredecessors(self,predecessors):
        self.predecessors = predecessors

    def remove_predecessor(self, predecessor):
        if predecessor in self.predecessors:
            self.predecessors.remove(predecessor)

    def add_successor(self, successor):
        if successor not in self.successors:
            self.successors.append(successor)

    def remove_successor(self, successor):
        if successor in self.successors:
            self.successors.remove(successor)
    
    def __str__(self):
        return f"Task {self.id}, {self.description}, duration: ({self.min}, {self.mode}, {self.max}), predecessors: {[predecessor.id for predecessor in self.predecessors]}, successors: {[sucsessors.id for sucsessors in self.successors]} , ES: {self.ES}, EF: {self.EF}, LS: {self.LS}, LF: {self.LF}, slack: {self.slack}, critical: {self.critical}"


class PERTdiagram:

    def __init__(self):

        self.criticalPath = []
        self.tasks = []

    def addTask(self,task):
        self.tasks.append(task)

    def removeTask(self,task):
        self.tasks.remove(task)

    def get_description_column_name(self, df):
        if 'Description' in df.columns:
            return 'Description'
        elif 'Descriptions' in df.columns:
            return 'Descriptions'
        else:
            raise ValueError("No 'Description' or 'Descriptions' column found in the DataFrame")

    def collectProjectFromExcel(self,excelFile,sheetname):
        df = pd.read_excel(excelFile, sheetname, header=0, index_col=None)
        description_column = self.get_description_column_name(df)

        for index, row in df.iterrows():
            if row.isnull().all():
                continue
            id = row['Codes']
            description = row[description_column] if row[description_column] else 'nan'
            duration = [int(d) for d in row['Durations'].strip('()').split(',')] if not isinstance(row['Durations'],float) else [0, 0, 0]
            cleaned_duration = [int(str(dur).strip(" ")) for dur in duration]
            predecessors = row['Predecessors'].split(', ') if not isinstance(row['Predecessors'],float) else []
            # print(id, description, duration, predecessors)
            if description and duration:
                task = Task(id, description, cleaned_duration, [])
            else:
                task = Task(id, '', [0, 0, 0], [])
            self.addTask(task)

        # Now that all tasks have been created, establish the connections between tasks based on predecessors
        for index, row in df.iterrows():
            if index < 1:
                continue
            task_id = row['Codes']
            predecessors = row['Predecessors'].split(', ') if not isinstance(row['Predecessors'],float) else []
            for predecessor_id in predecessors:
                if predecessor_id:  # Avoid empty predecessor strings
                    self.connect_tasks(predecessor_id, task_id)

    
    def connect_tasks(self, predecessor, successor):
        predecessor_task = self.find_task_by_id(predecessor)
        successor_task = self.find_task_by_id(successor)
        if predecessor_task and successor_task:
            predecessor_task.add_successor(successor_task)
            successor_task.add_predecessor(predecessor_task)

    def disconnect_tasks(self, predecessor, successor):
        predecessor_task = self.find_task_by_id(predecessor)
        successor_task = self.find_task_by_id(successor)

        if predecessor_task and successor_task:
            predecessor_task.remove_successor(successor_task)
            successor_task.remove_predecessor(predecessor_task)

    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


    def calculate(self):
        self.forwardPass()
        self.backwardPass()
        self.findCriticalPath()

    def forwardPass(self):
        for task in self.tasks:
            if task.id == 'Start':
                continue
            if task.predecessors == ['Start']:
                task.ES = 0
                task.EF = task.duration
            else:
                task.ES = max([t.EF for t in task.predecessors])
                task.EF = round(task.ES + task.duration,2)

    def backwardPass(self):
        for task in reversed(self.tasks):
            if len(task.successors) == 0:
                task.LF = task.EF
                task.LS = task.LF - task.duration
            else:
                task.LF = min([t.LS for t in task.successors])
                task.LS = round(task.LF - task.duration,2)

    def findCriticalPath(self):
        for task in self.tasks:
            task.slack = task.LS - task.ES
            if task.slack == 0:
                task.critical = True
                self.criticalPath.append(task)
    
    def printCriticalPath(self):
        print("Critical Path:")
        for task in self.criticalPath:
            print(task.id)
            
    def print_all_tasks(self):
        for task in self.tasks:
            print(task)


def main():
    pert = PERTdiagram()
    pert.collectProjectFromExcel('Warehouse.xlsx','Warehouse')
    #pert.collectProjectFromExcel('Villa.xlsx','Villa')
    pert.forwardPass()
    pert.backwardPass()
    pert.print_all_tasks()



main()