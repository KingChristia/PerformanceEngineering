# Discrete Event Simulator

import sys

class Action:
	def __init__(self, name, completionDate):
		self.name = name
		self.completionDate = completionDate

	def getName(self):
		return self.name

	def getCompletionDate(self):
		return self.completionDate

	def setCompletionDate(self, date):
		self.completionDate = date

class Scheduler:
	def __init__(self):
		self.actions = []

	def getActions(self):
		return self.actions

	def getNumberOfActions(self):
		return len(self.actions)
	
	def isEmpty(self):
		return len(self.actions)==0

	def insertAction(self, action):
		position = 0
		while position<self.getNumberOfActions():
			scheduledAction = self.actions[position]
			if action.getCompletionDate()<scheduledAction.getCompletionDate():
				break
			position += 1
		self.actions.insert(position, action)

	def popFirstAction(self):
		if self.isEmpty():
			return None
		return self.actions.pop(0)

class Simulator:
	def __init__(self):
		self.scheduler = Scheduler()

	def newAction(self, name, completionDate):
		action = Action(name, completionDate)
		self.scheduler.insertAction(action)
		return action

	def simulationLoop(self, missionTime):
		while not self.scheduler.isEmpty():
			action = self.scheduler.popFirstAction()
			if action.getCompletionDate()>missionTime:
				break
			self.performAction(action)

	def performAction(self, action):
		print("Performed an action")
		sys.stdout.write("{0:s}\t{1:d}\n".format(action.getName(), action.getCompletionDate()))
		name = action.getName() + "'"
		completionDate = action.getCompletionDate() + 5
		simulator.newAction(name, completionDate)
		
simulator = Simulator()
simulator.newAction("1", 10)
simulator.newAction("2", 20)
simulator.newAction("3", 15)
simulator.simulationLoop(40)
