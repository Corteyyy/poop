import telebot
from telebot import types
import random, pyexcel


bot = telebot.TeleBot("1657248539:AAH8T8DfOy27HwpBtBp__FQYb80HacfKu8c")


@bot.message_handler(commands=['start'])
def send_welcome(message):
	# клавиатура
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Регистрация")
	but2 = types.KeyboardButton("Найти человека")
	but3 = types.KeyboardButton("Найти команду")
	but4 = types.KeyboardButton("Мой ID")
	markup.add(but1, but2, but3, but4)

	bot.reply_to(message, "Здравствуй, {0.first_name}!\n Бот готов помочь тебе.".format(message.from_user),reply_markup=markup)
def get_info(message):
	global info,fio, id, f, job, room, id_command;
	try:
		room = ""
		clone = False
		info = message.text.replace(",", ";");
		info = info.split(";")
		fio = info[0]
		job = info[1]
		id_command = info[2]
		if int(info[2]) == 1:
			room = "Сайт для Драйв.Ру"
		elif int(info[2]) == 2:
			room = "Сайт для Lacoste"
		elif int(info[2]) == 3:
			room = "Редизайн для ГосУслуг"
		elif int(info[2]) == 4:
			room = "Сайт для Газпрома"
		else:
			bot.send_message(message.from_user.id, "Сверьтесь с примером и введите корректные данные.")
		if room != "":
			question = "Ваше ФИО:" + fio + "\n\nВаша должность:" + job + "\n\nНазвание вашей команды:" + room + "?"
			keyboard = types.InlineKeyboardMarkup();
			key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');
			keyboard.add(key_yes);
			key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
			keyboard.add(key_no);
			f = open('ID.txt', 'r+')
			for i in f:
				if fio in i.split(";")[1]:
					clone = True
					cloneId = "Вы уже регистрировались,ваш ID:" + i.split(";")[0]
					break
			if clone:
				bot.send_message(message.from_user.id, cloneId)
			else:
				bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
	except IndexError:
		bot.send_message(message.from_user.id, "Сверьтесь с примером и введите корректные данные.")

def id_check(message):
	fio = message.text
	f = open('ID.txt', 'r+')
	for i in f:
		if fio == i.split(";")[1] or fio == i.split(";")[0]:
			bot.send_message(message.from_user.id, "Ваш ID: " + str(i.split(";")[0]))
		else:
			return False

def find_dudes(message):
	info = message.text
	f = open('ID.txt', 'r+')
	for i in f:
		if info == i.split(";")[1] or info == i.split(";")[0]:
			bot.send_message(message.from_user.id, "Ваш Человек: " + str(i.split(";")[1]) + "\nЕго ID: "+ str(i.split(";")[0]))
		else:
			bot.send_message(message.from_user.id, "Такой человек не найден.")



@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.chat.type == 'private':
		if message.text == "Регистрация":
			bot.send_message(message.chat.id, "Хорошо, тогда введите ваше ФИО, должность и ID команды, к которой хотите подключиться."
											  "\n\nПример: Иванов Иван Иванович, дизайнер, 36")
			bot.register_next_step_handler(message, get_info);

		elif message.text == "Найти человека":
			bot.send_message(message.from_user.id, "Введите его ID или же его ФИО.")
			bot.register_next_step_handler(message, find_dudes)


		elif message.text == "Найти команду":
			inMurkup = types.InlineKeyboardMarkup(row_width=1)
			but1 = types.InlineKeyboardButton(
				"Сайт для Драйв.ру",
				callback_data='book1')
			but2 = types.InlineKeyboardButton("Сайт для Lacoste", callback_data='book2')
			but3 = types.InlineKeyboardButton("Редизайн ГосУслуг", callback_data='book3')
			but4 = types.InlineKeyboardButton("Сайт для Газпрома", callback_data='book4')
			inMurkup.add(but1, but2, but3, but4)
			bot.send_message(message.chat.id, "Вот доступные команды:", reply_markup=inMurkup)

		elif message.text == "Мой ID":
			bot.send_message(message.from_user.id, "Введите ваше ФИО.")
			bot.register_next_step_handler(message, id_check)


#обработка callback
@bot.callback_query_handler(func=lambda call: True)

def callback_inline(call):
	global id, f, room, id_command
	if call.data == "yes":
		hyper = ""
		id = random.randint(1, 1488)
		packet = str(id) + ";" + fio + ";" + job + ";" + id_command[1]
		f.write(packet + "\n")
		f.close()
		if int(id_command) == 1:
			hyper = "https://t.me/+-lrR94ZzoqoxZTdi"
		elif int(id_command) == 2:
			hyper = "https://t.me/+_2sA1D0Fgx8zOTgy"
		elif int(id_command) == 3:
			hyper = "https://t.me/+gM6jFzOfg8ZjZWMy"
		elif int(id_command) == 4:
			hyper = "https://t.me/+STObvw9LKpliNzEy"
		bot.send_message(call.message.chat.id, 'Вы зарегистрированы и присоединены к группе.\n\n Ваш ID: ' + str(id) + "\nСсылка для чата:" + hyper);
		array_with_excel = pyexcel.get_array(file_name=id_command[1]+".xls")
		array_append = [fio,job,str(id)]
		print(array_with_excel.append(array_append))
		pyexcel.save_as(array=array_with_excel, dest_file_name=id_command[1] + ".xls")
	elif call.data == "no":
		bot.send_message(call.message.chat.id, 'Тогда пройдите его заново, он небольшой.');
	elif call.data == "book1":
		bot.send_message(call.message.chat.id, 'Состав команды и их ID:')
		bot.send_document(call.message.chat.id, open('1.xls', 'rb'))
		bot.send_message(call.message.chat.id, "Ссылка на чат:"+'\nhttps://t.me/+-lrR94ZzoqoxZTdi')
	elif call.data == "book2":
		bot.send_message(call.message.chat.id, 'Состав команды и их ID:')
		bot.send_document(call.message.chat.id, open('2.xls', 'rb'))
		bot.send_message(call.message.chat.id, "Ссылка на чат:"+'\nhttps://t.me/+_2sA1D0Fgx8zOTgy')
	elif call.data == "book3":
		bot.send_message(call.message.chat.id, 'Состав команды и их ID:')
		bot.send_document(call.message.chat.id, open('3.xls', 'rb'))
		bot.send_message(call.message.chat.id, "Ссылка на чат:"+'\nhttps://t.me/+gM6jFzOfg8ZjZWMy')
	elif call.data == "book4":
		bot.send_message(call.message.chat.id, 'Состав команды и их ID:')
		bot.send_document(call.message.chat.id, open('4.xls', 'rb'))
		bot.send_message(call.message.chat.id, "Ссылка на чат:" + '\nhttps://t.me/+STObvw9LKpliNzEy')

bot.polling(none_stop=True)
