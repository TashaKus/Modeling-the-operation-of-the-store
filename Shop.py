import toga
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW, CENTER, Pack
from toga.colors import rgb
from random import randint, seed
from enum import Enum
import statistics as stat

State = Enum('State', 'shopping searching queued done fail')
model = None
avgServiceTime = []
avgLenQueue = []
cashBoxQueue = 0
clientDone = 0
clientLeave = 0
money = 0


def MultilineLabel( text : str,
                    box_style : Pack = None,
                    label_style : Pack = None,
                  ) -> toga.Box :
    
    box = toga.Box( id = None,
                    style = box_style,
                    children = [ toga.Label( t, style=label_style ) for t in text.split('/n') ]
                    )
    return box
    
'''def createBox( text : str,
				box_style : Pack = None,
				label_style : Pack = None,
			  ) -> toga.Box :
	text_label = toga.Label(text, style=label_style)
	text_input = toga.TextInput()
	box = toga.Box(style = box_style)
	box.add(text_label, text_input)
	return box
'''
	

class Model:
	def __init__(self, cashBoxCount, maxQueueLen):
		self.currentTime = 0
		self.customers = []
		self.shop = Shop(cashBoxCount, maxQueueLen)
		self.newCustomerTimer = randint(2,5)
	
	def tick(self):
		self.currentTime += 1
		self.shop.tick()
		self.newCustomerTimer -= 1
		if self.newCustomerTimer <= 0:
			newC = Customer(self.shop)
			self.customers.append(newC)
			self.shop.customers.append(newC)
			self.newCustomerTimer = randint(2,5)

class Shop:
	def __init__(self, cashBoxCount, maxQueueLen):
		self.cashBoxes = []
		self.customers = []
		for i in range(cashBoxCount):
			self.cashBoxes.append(CashBox())
		self.maxQueueLen = maxQueueLen
		
	def tick(self):
		#reversed?
		for i in self.customers:
			i.tick()
		for cb in self.cashBoxes:
			cb.tick()
			
		
	def findCashBox(self):
		global cashBoxQueue
		for i in range(cashBoxQueue, len(self.cashBoxes)):
			if len(self.cashBoxes[i].queue) < self.maxQueueLen:
				cashBoxQueue = (cashBoxQueue + 1) % len(self.cashBoxes)
				return self.cashBoxes[i]
		if cashBoxQueue > 0:
			for i in range(0, cashBoxQueue):
				if len(self.cashBoxes[i].queue) < self.maxQueueLen:
					cashBoxQueue = (cashBoxQueue + 1) % len(self.cashBoxes)
					return self.cashBoxes[i]
		return None
		
	def customerLeave(self, customer):
		global clientLeave
		self.customers.remove(customer)
		clientLeave += 1	
			

class CashBox:
	def __init__(self):
		self.serviceTimer = 0
		self.queue = []
	
	def tick(self):
		global avgLenQueue
		avgLenQueue.append(len(self.queue))
		if self.serviceTimer == 0 and len(self.queue) > 0:
			self.serviceTimer = randint(5, 15)
			avgServiceTime.append(self.serviceTimer)
		elif self.serviceTimer > 0:
			self.serviceTimer -= 1
			if self.serviceTimer == 0:
				self.queue[0].serviceDone()
				self.queue.pop(0)
			
	def enqueue(self, customer):
		self.queue.append(customer)
			
class Customer:
	def __init__(self, shop):
		self.shop = shop
		self.cash = randint(100,3000)
		self.state = State.shopping
		self.stateTimer = randint (5, 15)
		
	def tick(self):
		if self.state == State.queued:
			return
		self.stateTimer -= 1	
		if self.stateTimer <= 0:
			if self.state == State.shopping:
				self.state = State.searching
				self.stateTimer = randint (4, 7)
			elif self.state == State.searching:
				cb = self.shop.findCashBox()
				if cb == None:
					self.state = State.fail
					self.shop.customerLeave(self)
				else:
					self.state = State.queued
					cb.enqueue(self)
	
	def serviceDone(self):
		global clientDone, money
		money += self.cash
		self.shop.customers.remove(self)
		clientDone += 1



class MyApp(toga.App):
	
	def startup(self):
		
		main_window = toga.MainWindow(title=self.name, size=(1000, 400))
		
		def buttonStep_handler(widget):
			
			global model
			step = int(step_text.value)
			while step:
				model.tick()
				step -= 1
				
			global avgServiceTime, avgLenQueue, clientDone, clientLeave, money
			
			
			if len(avgServiceTime) == 0:
				aST = "0"
			else:
				aST = str(round(stat.mean(avgServiceTime), 3))
			if len(avgLenQueue) == 0:
				aLQ = "0"
			else:
				aLQ = str(round(stat.mean(avgLenQueue), 3))	
				
			money = money * int(profit_text.value) / 1000    #прибыль от покупок
			money = money - int(cashBoxNumber_text.value) * ((int(salary_text.value) / 24) * (int(step_text.value) / 60)) #зарплаты кассиров
			money = money - (int(sale_text.value) / 24) * (int(step_text.value) / 60)   #затраты на рекламу
			
			table.data = [['Среднее время обслуживания', aST, 'мин'], 
				['Средняя длина очереди касс', aLQ, 'чел'],
				['Кол-во обслуженных клиентов', str(clientDone), 'чел'],
				['Количество потерянных клиентов', str(clientLeave), 'чел'],
				['Общая прибыль', str(round(money, 3)), 'руб']]
				
			m = int(minute_label.text) + int(step_text.value)
			if m >= 60:
				if m-60 == 0:
					minute_label.text = "00"
				else:
					minute_label.text = str(m-60)
				h = int(hour_label.text) + 1
				if h >= 24:
					if h-24 == 0:
						hour_label.text = "00"
					else:
						hour_label.text = str(h - 24)
					if day_label.text == "пн":
						day_label.text = "вт"
					elif day_label.text == "вт":
						day_label.text == "ср"
					elif day_label.text == "ср":
						day_label.text == "чт"
					elif day_label.text == "чт":
						day_label.text == "пт"
					elif day_label.text == "пт":
						day_label.text == "сб"
					elif day_label.text == "сб":
						day_label.text == "вс"
					elif day_label.text == "вс":
						day_label.text == "конец"
						hour_label.text == "недели"
						minute_label.text == ""
				else:
					hour_label.text = str(h)
			else:
				minute_label.text = str(m)
		def buttonToEnd_handler(widget):
			print("hello")
		def buttonStop_handler(widget):
			print("hello")
		def buttonExit_handler(window):
			main_window.close()
			self.exit()
		def buttonBegin_handler(widget):
			global model
			model = Model(int(cashBoxNumber_text.value), int(maxQueueLen_text.value))
			
			day_label.text = "пн"
			hour_label.text = "00"
			minute_label.text = "00"
			
			#блокировка полей
		
			cashBoxNumber_text.readonly = True
			maxQueueLen_text.readonly = True
			advert_text.readonly = True
			sale_text.readonly = True
			salary_text.readonly = True
			minExpense_text.readonly = True
			maxExpense_text.readonly = True
			loss_text.readonly = True
			profit_text.readonly = True
			step_text.readonly = True
			buttonBegin.enabled = False
			button1.enabled = False
			button2.enabled = False
			button3.enabled = False
			button4.enabled = False
			button5.enabled = False
			button6.enabled = False
			button7.enabled = False
			button8.enabled = False
			button9.enabled = False
			button10.enabled = False
			
			
		#обработчики полей для ввода
		
		def enter1(widget):
			print(cashBoxNumber_text.value)
		def enter2(widget):
			print(maxQueueLen_text.value)
		def enter3(widget):
			print(advert_text.value)
		def enter4(widget):
			print(sale_text.value)
		def enter5(widget):
			print(salary_text.value)
		def enter6(widget):
			print(minExpense_text.value)
		def enter7(widget):
			print(maxExpense_text.value)
		def enter8(widget):
			print(loss_text.value)
		def enter9(widget):
			print(profit_text.value)
		def enter10(widget):
			print(step_text.value)
			
		# поля для ввода
		
		info_box = toga.Box()
		
		cashBoxNumber_box = toga.Box(style = Pack(direction=ROW))
		cashBoxNumber_text = toga.TextInput(initial = "3", style = Pack(flex=2))
		button1 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter1)
		cashBoxNumber_label = toga.Label('Количество касс :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		cashBoxNumber_box.add(cashBoxNumber_label, cashBoxNumber_text, button1)
		
		maxQueueLen_box = toga.Box(style = Pack(direction=ROW))
		maxQueueLen_text = toga.TextInput(initial = "3", style = Pack(flex=2))
		button2 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter2)
		maxQueueLen_label = toga.Label('Максимальная длина очереди :', style=Pack(flex =1, text_align=RIGHT, width = 210))
		maxQueueLen_box.add(maxQueueLen_label, maxQueueLen_text, button2)
		
		advert_box = toga.Box(style = Pack(direction=ROW))
		advert_text = toga.TextInput(initial = "7000", style = Pack(flex=2))
		button3 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter3)
		advert_label = toga.Label('Затраты на рекламу :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		advert_box.add(advert_label, advert_text, button3)
			
		sale_box = toga.Box(style = Pack(direction=ROW))
		sale_text = toga.TextInput(initial = "15", style = Pack(flex=2))
		button4 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter4)
		sale_label = toga.Label('Размер скидки :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		sale_box.add(sale_label, sale_text, button4)
		
		salary_box = toga.Box(style = Pack(direction=ROW))
		salary_text = toga.TextInput(initial = "1500", style = Pack(flex=2))
		button5 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter5)
		salary_label = toga.Label('Зарплата кассира(в день) :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		salary_box.add(salary_label, salary_text, button5)
			
		minExpense_box = toga.Box(style = Pack(direction=ROW))
		minExpense_text = toga.TextInput(initial = "100", style = Pack(flex=2))
		button6 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter6)
		minExpense_label = toga.Label('Мин. сумма на покупки :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		minExpense_box.add(minExpense_label, minExpense_text, button6)
			
		maxExpense_box = toga.Box(style = Pack(direction=ROW))
		maxExpense_text = toga.TextInput(initial = "3000", style = Pack(flex=2))
		button7 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter7)
		maxExpense_label = toga.Label('Макс. сумма на покупки :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		maxExpense_box.add(maxExpense_label, maxExpense_text, button7)
		
		loss_box = toga.Box(style = Pack(direction=ROW))
		loss_text = toga.TextInput(initial = "0.2", style = Pack(flex=2))
		button8 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter8)
		loss_label_box = MultilineLabel('Степень уменьшения клиентов /nпри макс. длине очереди :', 
			box_style = Pack(direction=COLUMN), 
			label_style = Pack(flex= 1, text_align=RIGHT, width = 210))
		loss_box.add(loss_label_box, loss_text, button8)
		
		profit_box = toga.Box(style = Pack(direction=ROW))
		profit_text = toga.TextInput(initial = "100", style = Pack(flex=2))
		button9 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter9)
		profit_label_box = MultilineLabel('Прибыль от покупки\nв 1000 рублей :', 
			box_style = Pack(direction=COLUMN), 
			label_style = Pack(flex= 1, text_align=RIGHT, width = 210))
		profit_box.add(profit_label_box, profit_text, button9)

		step_box = toga.Box(style = Pack(direction=ROW))
		step_text = toga.TextInput(initial = "15", style = Pack(flex=2))
		button10 = toga.Button("Ввести", style = Pack(flex=3), on_press = enter10)
		step_label = toga.Label('Шаг (10-60 мин.) :', style=Pack(flex= 1, text_align=RIGHT, width = 210))
		step_box.add(step_label, step_text, button10)
			
		buttonBegin = toga.Button('Начать', style = Pack(padding_left=80, padding_right=80, padding_top=20), on_press=buttonBegin_handler)
		curTime_box = toga.Box(style = Pack(direction=ROW,padding_top=20))
		curTime_label = toga.Label('Текущее время :', style = Pack(padding_left=60))
		day_label = toga.Label('День', style = Pack(padding_left=10))
		hour_label = toga.Label('Час')
		razd_label = toga.Label(' : ')
		minute_label = toga.Label('Минута')
		curTime_box.add(curTime_label, day_label, hour_label, razd_label, minute_label)

		info_box.add(cashBoxNumber_box, maxQueueLen_box, advert_box, sale_box, 
			profit_box, salary_box, loss_box, minExpense_box, maxExpense_box, 
			step_box, curTime_box, buttonBegin)
		info_box.style.update(direction=COLUMN, padding_top=10, padding_left=10, width=300)
		
		# кнопки
		
		buttonStep = toga.Button('Шаг', style = Pack(flex=1, padding_right=10, padding_left=10), on_press=buttonStep_handler)
		buttonStep.style.flex = 1
		buttonToEnd = toga.Button('До конца', style = Pack(flex=2, padding_right=10), on_press=buttonToEnd_handler)
		buttonToEnd.style.flex = 2
		buttonStop = toga.Button('Стоп', style = Pack(flex=3, padding_right=10), on_press=buttonStop_handler)
		buttonStop.style.flex = 3
		buttonExit = toga.Button('Выход', style = Pack(flex=4, padding_right=10), on_press=buttonExit_handler)
		buttonExit.style.flex = 4
		button_box = toga.Box()
		button_box.add(buttonStep, buttonToEnd, buttonStop, buttonExit)
		button_box.style.update(direction=ROW, padding_top=40, padding_bottom=10, padding_right=10, alignment = CENTER, height = 80)
		
		# кассы
		
		canvas = toga.Canvas()
		canvas_box = toga.Box()
		with canvas.fill(color=rgb(250, 119, 73)) as f:
			#for i in range(cashBoxNumber_box.t)
			f.rect(50, 100, 30, 20)
			f.rect(150, 100, 30, 20)
			f.rect(250, 100, 30, 20)
			
		# покупатели
		
		with canvas.fill(color=rgb(0, 119, 73)) as f:
			f.arc(100, 50, 5)
			f.arc(100, 70, 5)
			f.arc(100, 90, 5)
		with canvas.fill(color=rgb(0, 119, 73)) as f:
			f.arc(200, 90, 5)
			f.arc(300, 90, 5)
		canvas_box.add(canvas)
		canvas_box.style.update(height = 170, width = 600)
		
		# сводная таблица
		
		table = toga.Table([' ', 'Значение', 'Ед.измерения'])
		table.min_width = 600
		table.min_height = 500
		table.data = [['Среднее время обслуживания', '0', 'мин'], 
			['Средняя длина очереди касс', '0', 'чел'],
			['Кол-во обслуженных клиентов', '0', 'чел'],
			['Количество потерянных клиентов', '0', 'чел'],
			['Общая прибыль', '0', 'руб']]
		
		# моделирование
		
		work_box = toga.Box()
		work_box.add(canvas_box, table, button_box)
		work_box.style.update(direction=COLUMN, width = 600, padding_left=10)
		
		# все окно
		
		work_box.style.flex = 2
		info_box.style.flex = 1
		
		main_box = toga.Box()
		main_box.add(info_box, work_box)
		main_box.style.update(direction=ROW)
		
		main_window.content = main_box
		main_window.show()

if __name__ == '__main__':
    app = MyApp('Shop', 'org.beeware.helloworld')
    app.main_loop()

