# Queue

# 1. Imported Modules
# -------------------

import sys


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
		self.queue = Queue(1, 5)

	def getCustomers(self):
		return self.customers.values()

	def newCustomer(self):
		self.nextCustomerNumber += 1
		customer = Customer(self.nextCustomerNumber)
		self.customers[self.nextCustomerNumber] = customer
		return customer

	def lookForCustomer(self, identifier):
		return self.customers.get(identifier, None)

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
		outputFile.write("\n")

# 7. Test
# -------

shop = Shop()
for _ in range(10):
	shop.newCustomer()

C1 = shop.lookForCustomer(4)
shop.enqueueCustomer(C1)

C2 = shop.lookForCustomer(2)
shop.enqueueCustomer(C2)

C3 = shop.dequeueCustomer()


printer = Printer()
printer.printCustomers(shop, sys.stdout)


		

