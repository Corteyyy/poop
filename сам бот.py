# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from настройки import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

reply_keyboard = [['/Autobus', '/Nearest_Ostanovka'],
                      ['/Marshrut', '/My_mestopolozhenie']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )

def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Время вышло!')

def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return
        if due == 0:
            update.message.reply_text(
                'Нууу... Время вышло...')
            return

        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        # Запоминаем созданную задачу в данных чата.
        context.chat_data['job'] = new_job
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(f'Отсчёт в {due} секунд пошёл!')

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')

def unset_timer(update, context):
    # Проверяем, что задача ставилась
    if 'job' not in context.chat_data:
        update.message.reply_text('Нет активного таймера')
        return
    job = context.chat_data['job']
    # планируем удаление задачи (выполнится, когда будет возможность)
    job.schedule_removal()
    # и очищаем пользовательские данные
    del context.chat_data['job']
    update.message.reply_text('Таймер остановлен!')


def echo(update, context):
    update.message.reply_text("Работайте ,пожалуйста, с клавишами")

def start(update, context):
    update.message.reply_text(
        'Привет! Я бот "Умный транспорт", открой панель клавиш и ты увидишь мои функции!', reply_markup=markup)

def help(update, context):
    update.message.reply_text(
        "Ваше местоположение:")
    update.message.reply_photo(photo=open('Screenshot_10.png', "rb"))

def address(update, context):
    update.message.reply_text(
        "Маршрут автоебиса №12")
    update.message.reply_photo(photo=open('Screenshot_8.png', "rb"))


def phone(update, context):
    update.message.reply_text("Телефон: 89825949011")


def site(update, context):
    update.message.reply_text(
        "Сайт: https://yandex.com")



def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("My_mestopolozhenie", help))
    dp.add_handler(CommandHandler("Autobus", address))
    dp.add_handler(CommandHandler("Nearest_Ostanovka", phone))
    dp.add_handler(CommandHandler("Marshrut", site))
    dp.add_handler(CommandHandler("keyboard", keyboard))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True)
                   )
    # Регистрируем обработчик в диспетчере.
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()