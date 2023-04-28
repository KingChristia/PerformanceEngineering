# Machine Learning - Introduction
# Regressor.py
# by Antoine Rauzy
# Copyrights (c) 2022 NTNU
#
# This file is part of a presentation given in the framework of the DISCo project.
# It is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
# For details about this license, see https://creativecommons.org/licenses/by-nc/4.0/.

# Table of Contents
# -----------------
# 1. Required Modules
# 2. Functions to print results
# 3. Loading of training and test sets
# 4. Regression

# 1. Required Modules
# -------------------

import sys
import math
import numpy

# 3. Functions to print results
# -----------------------------

def ExportResults(actualRewards, predictedRewards, fileName):
    output = open(fileName, "w")
    PrintResults(actualRewards, predictedRewards, output)
    output.close()
    
def PrintResults(actualRewards, predictedRewards, output):
    output.write("Actual duration\tPredicted duration\n")
    for i in range(0, len(actualRewards)):
        output.write("{0:g}\t{1:g}\n".format(actualRewards[i], round(predictedRewards[i], 0)))
    output.write("\n")
    output.write("MAE\t{0:g}\n".format(metrics.mean_absolute_error(actualRewards, predictedRewards)))
    output.write("RMSE\t{0:g}\n".format(math.sqrt(metrics.mean_squared_error(actualRewards, predictedRewards))))
    output.write("R^2\t{0:g}\n".format(metrics.r2_score(actualRewards, predictedRewards)))

# 2. Loading of training and test sets
# ------------------------------------

trainingSet = numpy.genfromtxt("trainingSetRegression.csv")
trainingInstances = trainingSet[:, 0:-2]
trainingLabels = trainingSet[:, -1]

testSet = numpy.genfromtxt("testSetRegression.csv")
testInstances = testSet[:, 0:-2]
testLabels = testSet[:, -1]


# 4. Support Vector Machines
# --------------------------
from sklearn import metrics

from sklearn.svm import SVR
model = SVR()
model.fit(trainingInstances, trainingLabels)

predictedLabels = model.predict(testInstances)
PrintResults(testLabels, predictedLabels, sys.stdout)
ExportResults(testLabels, predictedLabels, "ResultsRegression.csv")



