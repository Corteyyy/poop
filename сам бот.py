import telebot
from telebot import types
import random
import os
import xlrd

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
	global info,fio, id, f, job;
	try:
		clone = False
		info = message.text.split(",");
		fio = info[0]
		job = info[1]
		question = "Ваше ФИО:" + fio + "\n\nВаша должность:" + job + "?"
		keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
		key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
		keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
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
		if fio in i:
			bot.send_message(message.from_user.id, "Ваш ID: " + str(i.split(";")[0]))
		else:
			return False

def find_dudes(message):
	info = message.text
	f = open('ID.txt', 'r+')
	for i in f:
		if info in i:
			bot.send_message(message.from_user.id, "Ваш Человек: " + str(i.split(";")[1]) + "\nЕго ID: "+ str(i.split(";")[0]))



@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.chat.type == 'private':
		if message.text == "Регистрация":
			bot.send_message(message.chat.id, "Хорошо, тогда введите ваше ФИО и должность."
											  "\n\nПример: Иванов Иван Иванович, дизайнер")
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

def callback_worker(call):
	global id, f
	if call.data == "yes":
		id = random.randint(1, 1488)
		packet = str(id) + ";" + fio + "," + job
		f.write(packet + "\n")
		f.close()
		bot.send_message(call.message.chat.id, 'Вы зарегестрированы.\n\n Ваш ID:');
		bot.send_message(call.message.chat.id, id);
	elif call.data == "no":
		bot.send_message(call.message.chat.id, 'Тогда пройдите его заново, он небольшой.');



bot.polling(none_stop=True)