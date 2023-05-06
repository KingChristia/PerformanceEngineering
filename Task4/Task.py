import random

class Task:

    def __init__(self, id, description, duration, predecessors, riskfactor):
        self.id = id if id is not None else 0
        self.description = description if description is not None else ""

        self.predecessors = predecessors #if predecessors is not None else []
        self.successors = [] 

        self.min = duration[0] if duration[0] is not None else 0
        self.mode = duration[1] if duration[1] is not None else 0
        self.max = duration[2] if duration[2] is not None else 0
        self.duration = self.mode if self.mode is not None else 0

        self.riskfactor = riskfactor if riskfactor is not None else 1

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
        self.actualmode = random.triangular(
            self.min, self.max, self.newmode)
        self.setDuration(self.actualmode)

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getPredecessors(self):
        return self.predecessors

    def addPredecessor(self, predecessor):
        if predecessor not in self.getPredecessors():
            self.getPredecessors().append(predecessor)

    def removePredecessor(self, predecessor):
        if predecessor in self.getPredecessors():
            self.getPredecessors().remove(predecessor)

    def getSuccessors(self):
        return self.successors

    def addSuccessor(self, successor):
        if successor not in self.getSuccessors():
            self.getSuccessors().append(successor)

    def removeSuccessor(self, successor):
        if successor in self.getSuccessors():
            self.getSuccessors().remove(successor)

    def getMin(self):
        return self.min

    def setMin(self, min):
        self.min = min

    def getMode(self):
        return self.mode

    def setMode(self, mode):
        self.mode = mode

    def getMax(self):
        return self.max

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration

    def getRiskfactor(self):
        return self.riskfactor

    def setRiskfactor(self, riskfactor):
        self.riskfactor = riskfactor

    def getES(self):
        return self.ES

    def setES(self, ES):
        self.ES = ES

    def getEF(self):
        return self.EF

    def setEF(self, EF):
        self.EF = EF

    def getLS(self):
        return self.LS

    def setLS(self, LS):
        self.LS = LS

    def getLF(self):
        return self.LF

    def setLF(self, LF):
        self.LF = LF

    def getSlack(self):
        return self.slack

    def setSlack(self, slack):
        self.slack = slack

    def getCritical(self):
        return self.critical

    def setCritical(self, critical):
        self.critical = critical

    def getLF(self):
        return self.LF





    def __str__(self):
        return f"Task {self.getId()}, {self.getDescription()}, duration: {round(self.getDuration())}, predecessors: {[predecessor.getId() for predecessor in self.getPredecessors()]}, successors: {[sucsessors.getId() for sucsessors in self.getSuccessors()]} , ES: {self.getES()}, EF: {self.getEF()}, LS: {self.getLS()}, LF: {self.getLF()}, slack: {self.getSlack()}, critical: {self.getCritical()}, riskfactor: {self.getRiskfactor()}"
