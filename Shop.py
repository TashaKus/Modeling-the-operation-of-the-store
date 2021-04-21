import toga
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW, CENTER, Pack
from toga.colors import rgb

def MultilineLabel( text : str,
                    box_style : Pack = None,
                    label_style : Pack = None,
                  ) -> toga.Box :
    
    box = toga.Box( id = None,
                    style = box_style,
                    children = [ toga.Label( t, style=label_style ) for t in text.split('/n') ]
                    )
    return box
    
def createBox( text : str,
				box_style : Pack = None,
				label_style : Pack = None,
			  ) -> toga.Box :
	text_label = toga.Label(text, style=label_style)
	text_input = toga.TextInput()
	box = toga.Box(style = box_style)
	box.add(text_label, text_input)
	return box

class MyApp(toga.App):
	def startup(self):
		self.main_window = toga.MainWindow(title=self.name, size=(1000, 400))
		
		def buttonStep_handler(widget):
			print("hello")
		def buttonToEnd_handler(widget):
			print("hello")
		def buttonStop_handler(widget):
			print("hello")
		def buttonExit_handler(widget):
			print("hello")
		def buttonBegin_handler(widget):
			print("hello")
		
		# поля для ввода
		info_box = toga.Box()
		
		cashBoxNumber_box = toga.Box(style = Pack(direction=ROW))
		cashBoxNumber_text = toga.TextInput()
		cashBoxNumber_label = toga.Label('Количество касс :', style=Pack(text_align=RIGHT, width = 210))
		cashBoxNumber_box.add(cashBoxNumber_label, cashBoxNumber_text)
		
		maxQueueLen_box = createBox('Максимальная длина очереди :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
			
		advert_box = createBox('Затраты на рекламу :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
			
		sale_box = createBox('Размер скидки :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
			
		salary_box = createBox('Зарплата кассира :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
			
		minExpense_box = createBox('Мин. сумма на покупки :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
		
		maxExpense_box = createBox('Макс. сумма на покупки :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
			
		loss_label = MultilineLabel('Степень уменьшения клиентов /nпри макс. длине очереди :', 
			box_style = Pack(direction=COLUMN), 
			label_style = Pack(text_align=RIGHT, width = 210))
		loss_box = toga.Box(style = Pack(direction=ROW))
		loss_box.add(loss_label, toga.TextInput())
		
					
		profit_label = MultilineLabel('Прибыль от покупки\nв 1000 рублей :', 
			box_style = Pack(direction=COLUMN), 
			label_style = Pack(text_align=RIGHT, width = 210))
		profit_box = toga.Box(style = Pack(direction=ROW))
		profit_box.add(profit_label, toga.TextInput())
			
		step_box = createBox('Шаг (мин.) :', 
			box_style = Pack(direction=ROW), 
			label_style = Pack(text_align=RIGHT, width = 210))
			
		buttonBegin = toga.Button('Начать', style = Pack(padding_left=80, padding_right=80, padding_top=20), on_press=buttonBegin_handler)
		curTime_label = toga.Label('Текущее время: День Час Минута', style = Pack(padding_left=10, padding_top=20))
		
		info_box.add(cashBoxNumber_box, maxQueueLen_box, advert_box, sale_box, 
			profit_box, salary_box, loss_box, minExpense_box, maxExpense_box, 
			step_box, curTime_label, buttonBegin)
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
		
		table = toga.Table(headings = [' ', 'Значение', 'Ед.измерения'])
		table.min_width = 600
		table.min_height = 500
		table.data.append('Среднее время обслуживания', '', 'мин')
		table.data.append('Средняя длина очереди касс', '', 'чел')
		table.data.append('Кол-во обслуженных клиентов', '', 'чел')
		table.data.append('Количество потерянных клиентов', '', 'чел')
		table.data.append('Общая прибыль', '', 'руб')
		
		#table.data.insert(2, 'Value 1', 'Value 2')
		
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
		
		self.main_window.content = main_box
		self.main_window.show()

if __name__ == '__main__':
    app = MyApp('Shop', 'org.beeware.helloworld')
    app.main_loop()
