# Queue

# 1. Imported Modules
# -------------------

import sys
import random


# 2. Customers
# ------------

class Customer:
	SHOPPING = 0
	WAITING = 1
	PROCESSING = 2
	SERVED = 3

	def __init__(self, identifier):
		self.identifier = identifier
		self.state = Customer.SHOPPING
		self.enqueueTime = -1

	def getIdentifier(self):
		return self.identifier

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def serializeState(self):
		if self.state==Customer.SHOPPING:
			return "shopping"
		if self.state==Customer.WAITING:
			return "waiting"
		if self.state==Customer.PROCESSING:
			return "processing"
		if self.state==Customer.SERVED:
			return "served"
		return "???"

	def getEnqueueTime(self):
		return self.enqueueTime

	def setEnqueueTime(self, time):
		self.enqueueTime = time

# 3. Queues
# ---------

class Queue:
	def __init__(self, number, capacity):
		self.number = number
		self.capacity = capacity
		self.cashier = None
		self.customers = []

	def getNumber(self):
		return self.number

	def getCapacity(self):
		return self.capacity

	def getCashier(self):
		return self.cashier
	
	def setCashier(self, cashier):
		self.cashier = cashier

	def isEmpty(self):
		return len(self.customers)==0

	def isFull(self):
		return len(self.customers)==self.capacity

	def getFirstCustomer(self):
		if self.isEmpty():
			return None
		return self.customers[0]
		
	def enqueueCustomer(self, customer):
		self.customers.append(customer)

	def dequeueCustomer(self):
		if self.isEmpty():
			return None
		return self.customers.pop(0)

# 4. Cashier
# ----------


# 5. Shop
# -------

class Shop:
	def __init__(self):
		self.customers = dict()
		self.nextCustomerNumber = 0
		self.queue = Queue(1, 100)

	def getCustomers(self):
		return self.customers.values()

	def newCustomer(self):
		self.nextCustomerNumber += 1
		customer = Customer(self.nextCustomerNumber)
		self.customers[self.nextCustomerNumber] = customer
		return customer

	def lookForCustomer(self, identifier):
		return self.customers.get(identifier, None)

	def getFirstCustomerInQueue(self):
		return self.queue.getFirstCustomer()

	def enqueueCustomer(self, customer):
		if self.queue.isFull():
			return
		self.queue.enqueueCustomer(customer)
		customer.setState(Customer.WAITING)

	def dequeueCustomer(self):
		customer = self.queue.dequeueCustomer()
		if customer==None:
			return
		customer.setState(Customer.PROCESSING)
		return customer

# 6. Printer
# ----------

class Printer:
	def __init__(self):
		self.separator = "\t"

	def printCustomers(self, shop, outputFile):
		for customer in shop.getCustomers():
			self.printCustomer(customer, outputFile)

	def printCustomer(self, customer, outputFile):
		outputFile.write("{0:d}".format(customer.getIdentifier()))
		outputFile.write(self.separator)
		outputFile.write("{0:s}".format(customer.serializeState()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getEnqueueTime()))
		outputFile.write("\n")

# 7. Events
# ---------

class Event:
	ENQUEUE_CUSTOMER = 1
	DEQUEUE_CUSTOMER = 2

	def __init__(self, type, customer, date):
		self.type = type
		self.customer = customer
		self.date = date

	def getType(self):
		return self.type

	def getCustomer(self):
		return self.customer

	def getDate(self):
		return self.date

	def setDate(self, date):
		self.date = date

# 8. Scheduler
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
			if event.getDate()<scheduledEvent.getDate():
				break
			position += 1
		self.events.insert(position, event)

	def popFirstEvent(self):
		if self.isEmpty():
			return None
		return self.events.pop(0)

# 9. Simulator
# ------------

class Simulator:
	def __init__(self):
		self.shop = Shop()
		self.scheduler = Scheduler()
		self.outputFile = None

	def getShop(self):
		return self.shop

	def newCustomer(self):
		customer = self.shop.newCustomer()
		enqueueTime = random.randint(1, 1000)
		event = Event(Event.ENQUEUE_CUSTOMER, customer, enqueueTime)
		self.scheduler.insertEvent(event)

	def simulationLoop(self, missionTime, fileName):
		try:
			self.outputFile = open(fileName, "w")
		except:
			sys.stderr.write("Unable to open file {0:s}".format(fileName))
			return 1
		while not self.scheduler.isEmpty():
			event = self.scheduler.popFirstEvent()
			if event.getDate()>missionTime:
				break
			self.performEvent(event)
		self.outputFile.close()
		self.outputFile = None
		return 0

	def performEvent(self, event):
		if event.getType()==Event.ENQUEUE_CUSTOMER:
			customer = event.getCustomer()
			date = event.getDate()
			customer.setEnqueueTime(date)
			self.shop.enqueueCustomer(customer)
			self.updateShop()
		elif event.getType()==Event.DEQUEUE_CUSTOMER:
			customer = event.getCustomer()
			date = event.getDate()
			# customer.setDequeueTime(date)
			self.shop.dequeueCustomer()
			self.updateShop()

	def updateShop(self):
		customer = self.shop.getFirstCustomerInQueue()
		if customer==None:
			return
		dequeueTime = customer.getEnqueueTime() + 20
		event = Event(Event.DEQUEUE_CUSTOMER, customer, dequeueTime)
		self.scheduler.insertEvent(event)
		
		
		

# 10. Test
# -------

simulator = Simulator()
for _ in range(10):
	simulator.newCustomer()

simulator.simulationLoop(100000, "trace.txt")

printer = Printer()
printer.printCustomers(simulator.getShop(), sys.stdout)


		

