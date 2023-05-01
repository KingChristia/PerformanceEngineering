# CustomerQueue
#
# The objective of this program is to simulate the service of customers into a queue.
# New customers arrive in the queue with a frequency that is normally distributed (Poisson process) of rate m minutes.
# It takes on average n minutes to serve a client (n is close to m).
# Only one customer can be served at a time.
# Customers are served first-in, first-out.
# The queue has an infinite capacity.

# 1. Imported Modules
# -------------------

import sys
import random


# 2. Customers
# ------------

class Customer:
	NONE = 0
	WAITING = 1
	SERVING = 2
	SERVED = 3

	def __init__(self, identifier):
		self.identifier = identifier
		self.state = Customer.NONE
		self.arrivalTime = -1
		self.startServiceTime = -1
		self.completeServiceTime = -1

	def getIdentifier(self):
		return self.identifier

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def serializeState(self):
		if self.state==Customer.NONE:
			return "None"
		if self.state==Customer.WAITING:
			return "waiting"
		if self.state==Customer.SERVING:
			return "serving"
		if self.state==Customer.SERVED:
			return "served"
		return "???"

	def getArrivalTime(self):
		return self.arrivalTime

	def setArrivalTime(self, time):
		self.arrivalTime = time

	def getStartServiceTime(self):
		return self.startServiceTime

	def setStartServiceTime(self, time):
		self.startServiceTime = time

	def getCompleteServiceTime(self):
		return self.completeServiceTime

	def setCompleteServiceTime(self, time):
		self.completeServiceTime = time

# 3. Queues
# ---------

class Queue:
	def __init__(self):
		self.waitingCustomers = []
		self.currentlyServedCustomer = None

	def getWaitingCustomers(self):
		return self.waitingCustomers

	def getNumberOfCustomersWaiting(self):
		return len(self.waitingCustomers)

	def getCurrentlyServedCustomer(self):
		return self.currentlyServedCustomer

	def enqueueNewCustomer(self, customer, time):
		self.waitingCustomers.append(customer)
		customer.setState(Customer.WAITING)
		customer.setArrivalTime(time)

	def dequeueFirstWaitingCustomer(self):
		return self.waitingCustomers.pop(0)

	def startCustomerService(self, customer, time):
		self.currentlyServedCustomer = customer
		customer.setState(Customer.SERVING)
		customer.setStartServiceTime(time)

	def completeCustomerService(self, customer, time):
		self.currentlyServedCustomer = None
		customer.setState(Customer.SERVED)
		customer.setCompleteServiceTime(time)

# 4. Events
# ---------

class Event:
	NONE = 0
	CUSTOMER_ARRIVAL = 1
	START_CUSTOMER_SERVICE = 2
	COMPLETE_CUSTOMER_SERVICE = 3

	def __init__(self, type, customer, time):
		self.type = type
		self.customer = customer
		self.time = time

	def getType(self):
		return self.type

	def setType(self, type):
		self.type = type

	def serializeType(self):
		if self.type==Event.NONE:
			return "None"
		if self.type==Event.CUSTOMER_ARRIVAL:
			return "customerArrival"
		if self.type==Event.START_CUSTOMER_SERVICE:
			return "startCustomerService"
		if self.type==Event.COMPLETE_CUSTOMER_SERVICE:
			return "completeCustomerService"
		return "???"

	def getCustomer(self):
		return self.customer

	def getTime(self):
		return self.time

	def setTime(self, time):
		self.time = time

# 5. Scheduler
# ------------

class Scheduler:
	def __init__(self):
		self.events = []

	def getEvents(self):
		return self.events

	def getNumberOfEvents(self):
		return len(self.events)
	
	def isEmpty(self):
		return len(self.events)==0

	def insertEvent(self, event):
		position = 0
		while position<self.getNumberOfEvents():
			scheduledEvent = self.events[position]
			if event.getTime()<scheduledEvent.getTime():
				break
			position += 1
		self.events.insert(position, event)

	def popFirstEvent(self):
		if self.isEmpty():
			return None
		return self.events.pop(0)

	def scheduleCustomerArrival(self, customer, time):
		event = Event(Event.CUSTOMER_ARRIVAL, customer, time)
		self.insertEvent(event)
		return event

	def scheduleStartCustomerService(self, customer, time):
		event = Event(Event.START_CUSTOMER_SERVICE, customer, time)
		self.insertEvent(event)
		return event

	def scheduleCompleteCustomerService(self, customer, time):
		event = Event(Event.COMPLETE_CUSTOMER_SERVICE, customer, time)
		self.insertEvent(event)
		return event

# 7. Printer
# ----------

class Printer:
	def __init__(self):
		self.separator = "\t"

	def printQueue(self, queue, outputFile):
		outputFile.write("Waiting customers\n")
		for customer in queue.getWaitingCustomers():
			self.printCustomer(customer, outputFile)
		outputFile.write("Served customer\n");
		customer = queue.getCurrentlyServedCustomer()
		if customer==None:
			outputFile.write("None\n")
		else:
			self.printCustomer(customer, outputFile)

	def printCustomer(self, customer, outputFile):
		outputFile.write("{0:s}".format(customer.getIdentifier()))
		outputFile.write(self.separator)
		outputFile.write("{0:s}".format(customer.serializeState()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getArrivalTime()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getStartServiceTime()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getCompleteServiceTime()))
		outputFile.write("\n")

	def printSchedule(self, scheduler, outputFile):
		outputFile.write("Scheduled events\n")
		for event in scheduler.getEvents():
			self.printEvent(event, outputFile)

	def printEvent(self, event, outputFile):
		outputFile.write("{0:s}".format(event.serializeType()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(event.getTime()))
		outputFile.write(self.separator)
		outputFile.write("{0:s}".format(event.getCustomer().getIdentifier()))
		outputFile.write("\n")

# 9. Simulator
# ------------

class Simulator:
	def __init__(self):
		self.queue = Queue()
		self.scheduler = Scheduler()
		self.printer = Printer()
		self.outputFile = sys.stdout
		self.customerMeanTimeBetweenArrivals = 2
		self.customerStandardDeviationArrivalIntervals = 1
		self.customerServiceTime = 2
		self.customers = []

	def getQueue(self):
		return self.queue

	def scheduleCustomerArrivals(self, numberOfCustomers):
		currentTime = 0
		for i in range(numberOfCustomers):
			customer = Customer("customer" + str(i+1))
			self.customers.append(customer)
			currentTime += random.gauss(self.customerMeanTimeBetweenArrivals, self.customerStandardDeviationArrivalIntervals)
			self.scheduler.scheduleCustomerArrival(customer, currentTime)

	def simulationLoop(self):
		while not self.scheduler.isEmpty():
			event = self.scheduler.popFirstEvent()
			self.performEvent(event)

	def performEvent(self, event):
		customer = event.getCustomer()
		time = event.getTime()
		if event.getType()==Event.CUSTOMER_ARRIVAL:
			self.queue.enqueueNewCustomer(customer, time)
			self.updateCustomerService(time)
		elif event.getType()==Event.START_CUSTOMER_SERVICE:
			self.queue.startCustomerService(customer, time)
			completionTime = time + self.customerServiceTime
			self.scheduler.scheduleCompleteCustomerService(customer, completionTime)
		elif event.getType()==Event.COMPLETE_CUSTOMER_SERVICE:
			self.queue.completeCustomerService(customer, time)
			self.updateCustomerService(time)

	def updateCustomerService(self, time):
		if self.queue.getCurrentlyServedCustomer()!=None:
			return
		if self.queue.getNumberOfCustomersWaiting()==0:
			return
		customer = self.queue.dequeueFirstWaitingCustomer()
		self.scheduler.scheduleStartCustomerService(customer, time)

	def printQueue(self):
		self.printer.printQueue(self.queue, self.outputFile)

	def printSchedule(self):
		self.printer.printSchedule(self.scheduler, self.outputFile)

	def printCustomerHistory(self):
		self.outputFile.write("Customers\n")
		for customer in self.customers:
			self.printer.printCustomer(customer, self.outputFile)

# 10. Test
# -------

simulator = Simulator()

simulator.scheduleCustomerArrivals(2)

simulator.simulationLoop()
simulator.printCustomerHistory()


