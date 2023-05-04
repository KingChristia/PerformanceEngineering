

import pandas as pd
import random
import numpy


class Task:

    def __init__(self, id, description, duration, predecessors, riskfactor):
        self.id = id
        self.description = description

        self.predecessors = predecessors
        self.successors = []

        self.min = duration[0]
        self.mode = duration[1]
        self.max = duration[2]
        self.duration = self.mode

        self.riskfactor = riskfactor

        self.ES = 0
        self.EF = 0
        self.LS = 0
        self.LF = 0
        self.slack = 0

        self.critical = False

    def setNewmode(self):
        if self.mode * self.riskfactor < self.min:
            self.newmode = self.min
        elif self.mode * self.riskfactor > self.max:
            self.newmode = self.max
        else:
            self.newmode = self.mode * self.riskfactor
        self.actualmode = round(random.triangular(
            self.min, self.max, self.newmode), 2)
        self.setDuration(self.actualmode)

    def setPredecessors(self, predecessors):
        self.predecessors = predecessors

    def add_predecessor(self, predecessor):
        if predecessor not in self.predecessors:
            self.predecessors.append(predecessor)

    def setPredecessors(self, predecessors):
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

    def setDuration(self, duration):
        self.duration = duration

    def getLF(self):
        return self.LF

    def __str__(self):
        return f"Task {self.id}, {self.description}, duration: {self.duration}, predecessors: {[predecessor.id for predecessor in self.predecessors]}, successors: {[sucsessors.id for sucsessors in self.successors]} , ES: {self.ES}, EF: {self.EF}, LS: {self.LS}, LF: {self.LF}, slack: {self.slack}, critical: {self.critical}, riskfactor: {self.riskfactor}"


class PERTdiagram:

    def __init__(self):

        self.criticalPath = []
        self.tasks = []
        self.shortestduration = 0
        self.modeduration = 0
        self.longestduration = 0
        self.riskfactor = 0
        self.actualduration = 0
        self.intermediategate = []

    def addTask(self, task):
        self.tasks.append(task)

    def setRiskfactor(self):
        rf = random.choice([0.8, 1.0, 1.2, 1.4])
        for task in self.tasks:
            task.riskfactor = rf
        self.riskfactor = rf

    def removeTask(self, task):
        self.tasks.remove(task)

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
            # print(id, description, duration, predecessors)
            if description and duration:
                task = Task(id, description, cleaned_duration,
                            [], self.riskfactor)
            else:
                task = Task(id, '', [0, 0, 0], [], self.riskfactor)
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

    def calculateDurations(self):
        for task in self.tasks:
            task.setDuration(task.min)
        self.calculate()
        self.minduration = self.find_task_by_id('End').getLF()
        for task in self.tasks:
            task.setDuration(task.mode)
        self.calculate()
        self.modeduration = self.find_task_by_id('End').getLF()
        for task in self.tasks:
            task.setDuration(task.max)
        self.calculate()
        self.maxduration = self.find_task_by_id('End').getLF()
        self.calculatActualDuration()
        self.print_all_tasks()
        self.printDurations()
        gate_task_id, gate_index = self.find_intermediate_gate()
        print(f"Intermediate gate can be placed after Task {gate_task_id} at index {gate_index} in the critical path.")

    def calculatActualDuration(self):
        self.setRiskfactor()
        for task in self.tasks:
            task.setNewmode()
        self.calculate()
        self.actualduration = self.find_task_by_id('End').getLF()

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
                task.EF = round(task.ES + task.duration, 2)

    def backwardPass(self):
        for task in reversed(self.tasks):
            if len(task.successors) == 0:
                task.LF = task.EF
                task.LS = task.LF - task.duration
            else:
                task.LF = min([t.LS for t in task.successors])
                task.LS = round(task.LF - task.duration, 2)

    def findCriticalPath(self):
        self.criticalPath.clear()
        for task in self.tasks:
            task.slack = task.LS - task.ES
            if task.slack == 0:
                task.critical = True
                self.criticalPath.append(task)
            else:
                task.critical = False
                

    def classifyProject(self):
        if self.actualduration <= self.modeduration * 1.05:
            self.category = "Successful"
        elif self.modeduration * 1.05 < self.actualduration <= self.modeduration * 1.15:
            self.category = "Acceptable"
        else:
            self.category = "Failed"
            
    def find_intermediate_gate(self):
        half_duration = self.modeduration / 2
        print("Half duration:", half_duration)
        cumulative_duration = 0
        print([task.id for task in self.criticalPath])
        
        for i, task in enumerate(self.criticalPath):
            cumulative_duration += task.duration
            if cumulative_duration >= half_duration:
                self.intermediategate = task
                return task.id, i
        return None, None

    def printCriticalPath(self):
        print("Critical Path:")
        for task in self.criticalPath:
            print(task.id)

    def print_all_tasks(self):
        for task in self.tasks:
            print(task)

    def printDurations(self):
        print(
            f"Shortest duration: {self.minduration}, Mode duration: {self.modeduration}, Actual duration: {self.actualduration} Longest duration: {self.maxduration}")


class Simulation:

    def __init__(self, simulations) -> None:
        self.simulations = simulations

    def run(self):
        PD = PERTdiagram()
        results_df = pd.DataFrame(
            columns=['Risk Factor', 'Duration', 'Project Result'])
        PD.collectProjectFromExcel('Warehouse.xlsx', 'Warehouse')
        for sim in range(self.simulations):
            PD.calculateDurations()
            PD.classifyProject()
            new_row = {'Risk Factor': PD.riskfactor,
                       'Duration': PD.actualduration,
                       'Project Result': PD.category}

            results_df = pd.concat(
                [results_df, pd.DataFrame([new_row])], ignore_index=True)

        results_df.to_csv('results.csv', index=False)

    def task4(self):

        results_df = pd.read_csv('results.csv')
        # Print the statistics of the durations and project results
        print('Duration statistics:')
        # KANSKJE Vi GJØR DET SELV SENERE
        print(results_df['Duration'].describe())
        print('Project result counts:')
        print(results_df['Project Result'].value_counts())
        #self.task5()

    def task5(self):
        instances = []      

        """
        SKJALG! JEG HAR LAGET EN FUNKSJON SOM FINNER INTERMEDIATE GATE FRA KODEN! LES UT KOMMENTARENE UNDER HVIS DU SKAL JOBBE VIDERE
        HAR LAGET GRUNNOPPSETTET FOR Å HENTE UT FRA CSV FILEN! 
        
        """
        data = pd.read_csv('results.csv')
        
            
        for i in range(data['Risk Factor']):#Range er for antall rader i csv
            risk_factor = data['Risk Factor']#Hentes ut fra CSV 
            early_completion_dates = 0#Må regnes ut fra upstream fra Intermediate gate
            project_class = 0  #Hentes ut fra CSV
            project_duration =  0 #Hentes ut fra CSV
            
            instance = {
                'risk_factor': risk_factor,
                'early_completion_dates': early_completion_dates,
                'project_class': project_class,
                'project_duration': project_duration
            }
            instances.append(instance)
        



def main():
    pert = PERTdiagram()
    pert.collectProjectFromExcel('Warehouse.xlsx', 'Warehouse')
    # pert.collectProjectFromExcel('Villa.xlsx','Villa')
    pert.calculateDurations()
    sim = Simulation(5)
    sim.run()
    sim.task4()
    print(pert.classifyProject())
    


main()

"""

First, let's propose several positions for the intermediate gate:

After completion of the requirements analysis and before the design phase begins.
After the design phase and before the implementation phase begins.
After the implementation phase and before the testing phase begins.
Now, let's generate a sample of instances on which machine learning techniques can be applied. We will create 100 instances with varying risk factors and early completion dates for tasks upstream of the chosen gate.

To generate the instances, we will use Python and the random.choice method from the random package to randomly assign one of the four possible risk factor values (low, medium, high, or very high) to each instance. We will also randomly generate early completion dates for tasks upstream of the gate.

python
Copy code
import random

risk_factors = ['low', 'medium', 'high', 'very_high']
instances = []

for _ in range(100):
    risk_factor = random.choice(risk_factors)
    early_completion_dates = [random.randint(1, 20), random.randint(21, 40), random.randint(41, 60)]
    project_class = random.choice(['successful', 'unsuccessful'])
    project_duration = random.randint(60, 120)
    
    instance = {
        'risk_factor': risk_factor,
        'early_completion_dates': early_completion_dates,
        'project_class': project_class,
        'project_duration': project_duration
    }
    instances.append(instance)
We will then split the instances into a training set (80% of the sample) and a test set (20% of the sample).

python
Copy code
train_set = instances[:80]
test_set = instances[80:]
Now, we will apply three different classification methods. Let's use Decision Trees, k-Nearest Neighbors, and Support Vector Machines.

Decision Trees:
python
Copy code
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X_train = [instance['early_completion_dates'] for instance in train_set]
y_train = [instance['project_class'] for instance in train_set]
X_test = [instance['early_completion_dates'] for instance in test_set]
y_test = [instance['project_class'] for instance in test_set]

dt_clf = DecisionTreeClassifier()
dt_clf.fit(X_train, y_train)

y_pred = dt_clf.predict(X_test)
dt_accuracy = accuracy_score(y_test, y_pred)
k-Nearest Neighbors:
python
Copy code
from sklearn.neighbors import KNeighborsClassifier

knn_clf = KNeighborsClassifier(n_neighbors=3)
knn_clf.fit(X_train, y_train)

y_pred = knn_clf.predict(X_test)
knn_accuracy = accuracy_score(y_test, y_pred)
Support Vector Machines:
python
Copy code
from sklearn.svm import SVC

svm_clf = SVC(kernel='linear')
svm_clf.fit(X_train, y_train)

y_pred = svm_clf.predict(X_test)
svm_accuracy = accuracy_score(y_test, y_pred)
Finally, we can report and discuss the results:

python
Copy code
print(f"Decision Trees Accuracy: {dt_accuracy:.2f}")
print(f"k-Nearest Neighbors Accuracy: {knn_accuracy:.2f}")
print(f"Support Vector Machines Accuracy: {svm_accuracy:.2f}")
The above code will output the accuracy of each classifier. The accuracy may vary due to the randomness in generating instances. By comparing the accuracy scores of the three classification methods, we can determine which method performs best on this particular dataset. This information can be helpful for choosing the most appropriate classification method for future project management tasks.






We will use the same sample of instances generated above to apply three different regression methods: Linear Regression, Decision Tree Regression, and Support Vector Regression.

Linear Regression:
python
Copy code
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X_train = [instance['early_completion_dates'] for instance in train_set]
y_train = [instance['project_duration'] for instance in train_set]
X_test = [instance['early_completion_dates'] for instance in test_set]
y_test = [instance['project_duration'] for instance in test_set]

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
lr_mse = mean_squared_error(y_test, y_pred)
Decision Tree Regression:
python
Copy code
from sklearn.tree import DecisionTreeRegressor

dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)

y_pred = dtr.predict(X_test)
dtr_mse = mean_squared_error(y_test, y_pred)
Support Vector Regression:
python
Copy code
from sklearn.svm import SVR

svr = SVR(kernel='linear')
svr.fit(X_train, y_train)

y_pred = svr.predict(X_test)
svr_mse = mean_squared_error(y_test, y_pred)
Now, we can report and discuss the results:

python
Copy code
print(f"Linear Regression Mean Squared Error: {lr_mse:.2f}")
print(f"Decision Tree Regression Mean Squared Error: {dtr_mse:.2f}")
print(f"Support Vector Regression Mean Squared Error: {svr_mse:.2f}")
The above code will output the mean squared error (MSE) of each regression method. The MSE may vary due to the randomness in generating instances. By comparing the MSE scores of the three regression methods, we can determine which method performs best on this particular dataset. This information can be helpful for choosing the most appropriate regression method for future project management tasks.

Keep in mind that a lower MSE indicates a better fit, as it implies that the model's predictions are closer to the actual values. Additionally, other metrics like R-squared or mean absolute error could be used to evaluate and compare the performance of these regression models.
"""
