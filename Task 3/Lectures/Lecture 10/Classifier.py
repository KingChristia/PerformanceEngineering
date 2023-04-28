# Machine Learning - Introduction
# Classifier.py
# by Antoine Rauzy
# Copyrights (c) 2022 NTNU
#
# Table of Contents
# -----------------
# 1. Required Modules
# 2. Functions to print results
# 3. Loading of training and test sets
# 4. Classification

# 1. Required Modules
# -------------------

import sys
import numpy

# 3. Functions to print results
# -----------------------------

def ExportConfusionMatrix(labels, actualLabels, predictedLabels, fileName):
    output = open(fileName, "w")
    PrintConfusionMatrix(labels, actualLabels, predictedLabels, output)
    output.close()

def PrintConfusionMatrix(labels, actualLabels, predictedLabels, output):
    numberOfLabels = len(labels)
    counts = [[0 for _ in range(0, numberOfLabels)] for _ in range(0, numberOfLabels)]
    for i in range(0, len(actualLabels)):
        counts[int(actualLabels[i])][int(predictedLabels[i])] += 1
    for column in range(0, numberOfLabels):
        output.write("\t{0:s}".format(labels[column]))
    output.write("\n")
    for row in range(0, numberOfLabels):
        output.write("{0:s}".format(labels[row]))
        for column in range(0, numberOfLabels):
            output.write("\t{0:d}".format(counts[row][column]))
        output.write("\n")

# 2. Loading of training and test sets
# ------------------------------------

trainingSet = numpy.genfromtxt("Task_3/Lecture_10/trainingSetClassification.csv")
trainingInstances = trainingSet[:, 0:-2]
trainingLabels = trainingSet[:, -1]

testSet = numpy.genfromtxt("Task_3/Lecture_10/testSetClassification.csv")
testInstances = testSet[:, 0:-2]
testLabels = testSet[:, -1]

# 4. Classification
# -------------------

# from sklearn.svm import SVC
# model = SVC()
# model.fit(trainingInstances, trainingLabels)

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(trainingInstances, trainingLabels)

# from sklearn.neural_network import MLPClassifier
# model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
# model.fit(trainingInstances, trainingLabels)

predictedLabels = model.predict(testInstances)
PrintConfusionMatrix(["on-time", "delayed", "failed"], testLabels, predictedLabels, sys.stdout)
ExportConfusionMatrix(["on-time", "delayed", "failed"], testLabels, predictedLabels, "ResultsClassification.csv")
