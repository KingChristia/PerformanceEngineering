

import pandas as pd
import random
import sys
import numpy
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor

import ast

import PERTDiagram
import Printer


class Simulation:

    def __init__(self, simulations, excelFile, filePage) -> None:
        self.simulations = simulations
        self.excelFile = excelFile + '.xlsx'
        self.PERTdiagram = PERTDiagram.PERTdiagram()
        self.filePage = filePage
        self.xtrain = []
        self.ytrain = []
        self.xtest = []
        self.ytest = []
        self.trainset = []
        self.testset = []
        self.printer = Printer.Printer(sys.stdout)
        self.initializeTasks()

    def initializeTasks(self):
        self.getPERTdiagram().collectProjectFromExcel(
            self.getExcelfile(), self.getFilePage())

    def setSimulations(self, simulations):
        self.simulations = simulations

    def getSimulations(self):
        return self.simulations

    def setExcelfile(self, excelFile):
        self.excelFile = excelFile

    def getExcelfile(self):
        return self.excelFile

    def setPERTdiagram(self, PD):
        self.PERTdiagram = PD

    def getPERTdiagram(self):
        return self.PERTdiagram

    def setFilePage(self, page):
        self.filePage = page

    def getFilePage(self):
        return self.filePage

    def setXtrain(self, xtrain):
        self.xtrain = xtrain

    def getXtrain(self):
        return self.xtrain

    def setYtrain(self, ytrain):
        self.ytrain = ytrain

    def getYtrain(self):
        return self.ytrain

    def setXtest(self, xtest):
        self.xtest = xtest

    def getXtest(self):
        return self.xtest

    def setYtest(self, ytest):
        self.ytest = ytest

    def getYtest(self):
        return self.ytest

    def setTrainset(self, trainset):
        self.trainset = trainset

    def getTrainset(self):
        return self.trainset

    def setTestset(self, testset):
        self.testset = testset

    def getTestset(self):
        return self.testset

    def setPrinter(self, printer):
        self.printer = printer

    def getPrinter(self):
        return self.printer

    # Tasks

    # Task 4
    def task4(self, filename):
        resultsDF = pd.read_csv(filename + '.csv')
        actualdurationsummary = resultsDF['Actual duration'].describe()
        self.getPrinter().printTask4(actualdurationsummary, resultsDF)

    # Task5
    def task5(self, filename):
        self.createTrainingData(filename)
        dtaccuracy = self.createDecisionTree()
        knnaccuracy = self.createKNN()
        svmaccuracy = self.createSVM()
        self.getPrinter().printTask5(dtaccuracy, knnaccuracy, svmaccuracy)

    # Task6
    def task6(self, filename):
        self.createTrainingData(filename)
        lrmse = self.linearRegression()
        dtrmse = self.decisionTreeClassifier()
        svrmse = self.supportVectorRegression()
        self.getPrinter().printTask6(lrmse, dtrmse, svrmse)

    # Methods

    def createCSV(self, filename, intermediateGatePosition):
        resultsDF = pd.DataFrame(columns=[
                                 'Risk Factor', 'Early Completion Dates', 'Project Result', 'Actual duration'])

        for sim in range(self.getSimulations()):
            self.getPERTdiagram().calculateDurations()
            self.getPERTdiagram().setIntermediateGate(intermediateGatePosition)
            # Data we want to save to csv
            newrow = {'Risk Factor': self.getPERTdiagram().getRiskFactor(),
                      'Early Completion Dates': self.getPERTdiagram().getEarlyCompletionDates()[:intermediateGatePosition],
                      'Project Result': self.getPERTdiagram().classifyProject(),
                      'Actual duration': self.getPERTdiagram().getActualDuration()
                      }
            # Adds the data to the dataframe
            resultsDF = pd.concat(
                [resultsDF, pd.DataFrame([newrow])], ignore_index=True)
        # Saves the dataframe to a csv file
        resultsDF.to_csv(filename + ".csv", index=False)
        self.getPERTdiagram().createAndVisualizeGraphWithDepth(filename + '.png')

    def createTrainingData(self, filename):
        instances = []
        data = pd.read_csv(filename + '.csv')

        for i in range(data['Risk Factor'].count()):
            riskfactor = data['Risk Factor'][i]
            earlycompletiondates = ast.literal_eval(
                data['Early Completion Dates'][i])
            projectclass = data['Project Result'][i]
            projectduration = data['Actual duration'][i]

            instance = {
                'early completion dates': earlycompletiondates,
                'project class': projectclass,
                'risk factor': riskfactor,
                'project duration': projectduration,
            }
            instances.append(instance)

        # Creating the training and test sets
        self.setTrainset(instances[:int(len(instances) * 0.8)])
        self.setTestset(instances[int(len(instances) * 0.8):])

        self.setXtrain([instance['early completion dates']
                        for instance in self.getTrainset()])
        self.setYtrain([instance['project class']
                       for instance in self.getTrainset()])
        self.setXtest([instance['early completion dates']
                      for instance in self.getTestset()])
        self.setYtest([instance['project class']
                      for instance in self.getTestset()])

    def createDecisionTree(self):
        # Decision Tree Classifier
        dtclf = DecisionTreeClassifier()
        dtclf.fit(self.getXtrain(), self.getYtrain())

        ypred = dtclf.predict(self.getXtest())
        dtaccuracy = accuracy_score(self.getYtest(), ypred)
        return dtaccuracy

    def createKNN(self):
        knnclf = KNeighborsClassifier(n_neighbors=5)
        knnclf.fit(self.getXtrain(), self.getYtrain())

        ypred = knnclf.predict(self.getXtest())
        knnaccuracy = accuracy_score(self.getYtest(), ypred)
        return knnaccuracy

    def createSVM(self):
        svmclf = SVC(kernel='linear')
        svmclf.fit(self.getXtrain(), self.getYtrain())

        ypred = svmclf.predict(self.getXtest())
        svmaccuracy = accuracy_score(self.getYtest(), ypred)
        return svmaccuracy

        # Regression
    def getRegressionData(self):
        xtrain = [instance['early completion dates']
                  for instance in self.getTrainset()]
        ytrain = [instance['project duration']
                  for instance in self.getTrainset()]
        xtest = [instance['early completion dates']
                 for instance in self.getTestset()]
        ytest = [instance['project duration']
                 for instance in self.getTestset()]

        return xtrain, ytrain, xtest, ytest

    def linearRegression(self):
        lr = LinearRegression()
        xtrain, ytrain, xtest, ytest = self.getRegressionData()
        lr.fit(xtrain, ytrain)
        ypred = lr.predict(xtest)
        lrmse = mean_squared_error(ytest, ypred)
        return lrmse

    def decisionTreeClassifier(self):
        dtr = DecisionTreeRegressor()
        xtrain, ytrain, xtest, ytest = self.getRegressionData()
        dtr.fit(xtrain, ytrain)
        ypred = dtr.predict(xtest)
        dtrmse = mean_squared_error(ytest, ypred)
        return dtrmse

    def supportVectorRegression(self):
        svr = SVR(kernel='linear')
        xtrain, ytrain, xtest, ytest = self.getRegressionData()
        svr.fit(xtrain, ytrain)
        ypred = svr.predict(xtest)
        svrmse = mean_squared_error(ytest, ypred)
        return svrmse

    # numberOfSimulations is a list of the number of simulations we want to run
    def multipleSimulations(self, numberOfSimulations, filenamecsv, filename, sheet, intermediateGatePosition):
        dtaccuracylist = []
        knnaccuracylist = []
        svmaccuracylist = []
        lrmselist = []
        dtrmselist = []
        svrmselist = []
        simulationlist = []

        for number in numberOfSimulations:
            simulation = Simulation(number, filename, sheet)
            self.getPERTdiagram().setIntermediateGate(intermediateGatePosition)
            simulation.createCSV(
                filenamecsv, self.getPERTdiagram().getIntermediateGate())

            # Creates the simulation data
            simulation.createTrainingData(filenamecsv)

            dtaccuracy = simulation.createDecisionTree()
            knnaccuracy = simulation.createKNN()
            svmaccuracy = simulation.createSVM()

            lrmse = simulation.linearRegression()
            dtrmse = simulation.decisionTreeClassifier()
            svrmse = simulation.supportVectorRegression()

            simulationlist.append(number)
            dtaccuracylist.append(dtaccuracy)
            knnaccuracylist.append(knnaccuracy)
            svmaccuracylist.append(svmaccuracy)
            lrmselist.append(lrmse)
            dtrmselist.append(dtrmse)
            svrmselist.append(svrmse)

        # Add all values to a plot

        plt.plot(simulationlist, dtaccuracylist,
                 label="Decision Tree Accuracy")
        plt.plot(simulationlist, knnaccuracylist, label="KNN Accuracy")
        plt.plot(simulationlist, svmaccuracylist, label="SVM Accuracy")
        plt.legend()
        plt.xlabel("Number of Simulations")
        plt.xlim(numberOfSimulations[0], numberOfSimulations[-1])
        plt.ylabel("Accuracy")
        plt.title("Classifier Accuracies for different amount of simulations")
        # Save the first plot as a PNG file
        plt.savefig("classifierAccuracies.png")
        plt.clf()  # Clear the current figure for the next plot

        # Second plot
        plt.plot(simulationlist, lrmselist, label="Linear Regression MSE")
        plt.plot(simulationlist, dtrmselist,
                 label="Decision Tree Regression MSE")
        plt.plot(simulationlist, svrmselist,
                 label="Support Vector Regression MSE")
        plt.legend()
        plt.xlabel("Number of Simulations")
        plt.xlim(numberOfSimulations[0], numberOfSimulations[-1])
        plt.ylabel("Mean Squared Error")
        plt.title("Regression Mean Squared Errors, lower is better")
        plt.savefig("regressionMses.png")  # Save the second plot as a PNG file
        plt.clf()  # Clear the current figure if you want to create more plots


def task1to3():
    sim = Simulation(1, 'Warehouse', 'Warehouse')
    print("\n\nStart of simulation Warehouse\n\n")
    sim.getPERTdiagram().calculateDurations()

    sim.getPrinter().printAllTasks(sim.getPERTdiagram().getTasks())
    sim.getPrinter().printDurations(sim.getPERTdiagram())
    sim.getPrinter().printCriticalPath(sim.getPERTdiagram())
    print("\n\n Start of simulation Villa\n\n")
    sim2 = Simulation(1, 'Villa', 'Villa')
    sim2.getPERTdiagram().calculateDurations()

    sim2.getPrinter().printAllTasks(sim2.getPERTdiagram().getTasks())
    sim2.getPrinter().printDurations(sim2.getPERTdiagram())
    sim2.getPrinter().printCriticalPath(sim2.getPERTdiagram())


def task4to6():
    sim = Simulation(1000, 'Villa', 'Villa')
    # Proposed intermediate gates: [1, 5, 9, 12, 13, 14, 15, 18, 23, 28, 36, 37, 45, 49, 50, 59, 60, 61]
    sim.createCSV('lateresults', 36)
    sim.createCSV('earlyresults', 12)

    print("\n\nStatistics for early gate")
    print("-------------------------")
    sim.task4('earlyresults')
    print("\n\nMachine Learning for classification early gate")
    print("----------------------------------------------")
    sim.task5('earlyresults')
    print("\n\nMachine Learning for regression early gate")
    print("------------------------------------------")
    sim.task6('earlyresults')
    print("\n\n\n\n")
    print("\nStatistics for late gate")
    print("------------------------")
    sim.task4('lateresults')
    print("\n\nMachine Learning for classification late gate")
    print("---------------------------------------------")
    sim.task5('lateresults')
    print("\n\nMachine Learning for regression late gate")
    print("-----------------------------------------")
    sim.task6('lateresults')
    print("\n\n")

    # This method can be used to run multiple simulations and create plots to show how the ML algorithms perform with different amount of simulations

    # sim.multipleSimulations([100, 500, 1000, 2000, 4000, 8000, 16000, 32000],
    #                       'multipleresults', 'Villa', 'Villa', 36)


def main():
    task1to3()
    task4to6()


main()
