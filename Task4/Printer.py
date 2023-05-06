class Printer:

    def __init__(self, outputlocation) -> None:
        self.outputlocation = outputlocation

    def setOutputLocation(self, location):
        self.outputlocation = location

    def getOutputLocation(self):
        return self.outputlocation

    # methods

    def printCriticalPath(self, PD):
        print("Critical Path:", [task.getId() for task in PD.getCriticalPath()])



    def printAllTasks(self, tasks):
        for task in tasks:
            print([i.getId() for i in task.getPredecessors()],
                  task.getId(), [i.getId() for i in task.getSuccessors()])
            print(task)

    def printDurations(self, PD):
        print(f"Shortest duration: {PD.getShortestDuration()}, Mode duration: {PD.getModeDuration()}, Actual duration: {PD.getActualDuration()} Longest duration: {PD.getLongestDuration()}")

    def printTask4(self,actualdurationsummary,resultsDF):
        print('Duration statistics:')
        print(actualdurationsummary)
        print('Project result counts:')
        print(resultsDF['Project Result'].value_counts())
    
    def printTask5(self, dtaccuracy,knnaccuracy,svmaccuracy):
        print(f"Decision Trees Accuracy: {dtaccuracy:.2f}")
        print(f"k-Nearest Neighbors Accuracy: {knnaccuracy:.2f}")
        print(f"Support Vector Machines Accuracy: {svmaccuracy:.2f}")

    def printTask6(self, lrmse,dtrmse,svrmse):
        print(f"Linear Regression Mean Squared Error: {lrmse:.2f}")
        print(f"Decision Tree Regression Mean Squared Error: {dtrmse:.2f}")
        print(f"Support Vector Regression Mean Squared Error: {svrmse:.2f}")
