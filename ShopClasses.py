import random

class Model:
	def __init__(self, CashBoxCount, maxQueueLen):
		self.currentTime = 0
		self.customers = []
		self.shop = Shop(cashBoxCount, maxQueueLen)
		self.rnd = random.seed()
		self.newCustomerTimer = rnd(2,6)
	
	def tick(self):
		currentTime += 1
		shop.tick()
		if newCustomer-1 <= 0:
			customers.append(Customer(rnd, shop))
			newCustomerTimer = rnd(2, 6)
	
class Shop:
	def __init__(self, cashBoxCount, maxQueueLen, rnd):
		self.cashBoxes = []
		self.customers = []
		for i in range(cashBoxCount):
			cashBoxes.append(CashBox(rnd))
		self.maxQueueLen = maxQueueLen
		
	def tick():
		for i in reversed(customers.size):
			customers[i].tick()
		for cb in cashBoxes:
			cb.tick()
			
class CashBox:
	def __init__(self, rnd):
		self.rnd = rnd
		self.serviceTime = 0
		self.queue = []
	
	def tick():
		if serviceTime == 0 && queue.size > 0:
			serviceTime = rnd(5, 16)
		elif serviceTimer > 0:
			serviceTimer -= 1
			if serviceTimer == 0:
				Customer c = queue.dequeue()
				c.ServiceDone()
				
class Customer:
	def __init__(self, rnd, shop):
		self.rnd = rnd
		self.shop = shop
		shop.newCustomer(self)
		self.cash = rnd(100,3000)
		self.state = State.shopping
		self.stateTimer = rnd(5, 16)
		
	tick():
		if state == State.queued:
			return
		if stateTimer-1 <=0:
			if state = State.shopping:
				state = state.searching
				stateTimer = rhd(5, 11)
			elif state = State.searching:
				CashBox cb = shop.findCashBox()
				if cb == None:
					state = State.fail
					sop.customerLeave(self)
				else:
					state = State.queued
					cb.Enqueue(self)

