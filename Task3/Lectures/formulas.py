# Formulas

# 1. Imported modules
# -------------------

import sys


# 2. Formulas
# -----------

class Formula:
    def __init__(self):
        self.value = None

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value

class Constant(Formula):
    def __init__(self, value):
        Formula.__init__(self)
        self.setValue(value)

class Variable(Formula):
    def __init__(self, name):
        Formula.__init__(self)
        self.name = name

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

class Addition(Formula):
    def __init__(self, argument1, argument2):
        Formula.__init__(self)
        self.argument1 = argument1
        self.argument2 = argument2

    def getArgument1(self):
        return self.argument1
    
    def setArgument1(self, argument1):
        self.argument1 = argument1

    def getArgument2(self):
        return self.argument2
    
    def setArgument2(self, argument2):
        self.argument2 = argument2

# 3. Printer
# ----------

class Printer:
    def printFormula(self, formula, outputFile):
        if isinstance(formula, Constant):
            outputFile.write("{0:d}".format(formula.getValue()))
        elif isinstance(formula, Variable):
            outputFile.write("{0:s}".format(formula.getName()))
        elif isinstance(formula, Addition):
            outputFile.write("(")
            self.printFormula(formula.getArgument1(), outputFile)
            outputFile.write(" + ")
            self.printFormula(formula.getArgument2(), outputFile)
            outputFile.write(")")

# 4. Calculator
# -------------

class Calculator:
    def __init__(self, p):
        self.p = p

    def getP(self):
        return self.p

    def setP(self, p):
        self.p = p

    def calculateValue(self, formula):
        if isinstance(formula, Constant):
            result = formula.getValue() % self.p
        elif isinstance(formula, Variable):
            result = formula.getValue()
        elif isinstance(formula, Addition):
            value1 = self.calculateValue(formula.getArgument1())
            value2 = self.calculateValue(formula.getArgument2())
            if value1==None or value2==None:
                result = None
            else:
                result = (value1 + value2) % self.p
        else:
            result = None
        return result

# 5. Test
# -------

x = Variable("x")
y = Variable("y")
f1 = Addition(x, y)
c = Constant(1)
f2 = Addition(f1, c)

# printer = Printer()
# printer.printFormula(f2, sys.stdout)

x.setValue(1)
y.setValue(1)
calculator = Calculator(2)
value = calculator.calculateValue(f2)
print(value)
    
