import telebot
from telebot import types
from currency_converter import CurrencyConverter

currency = CurrencyConverter()
bot = telebot.TeleBot('7335512848:AAE5B-5NzCIrYinjbnrUhSzmC-HRMxRPFvQ')
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='USD/GBP')
        btn7 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn7)
        bot.send_message(message.chat.id, 'Выберите валюту', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0. Введите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете ввести новое значение')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валют через слеш ("/")')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    global amount
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете ввести новое значение')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Введите через слеш.')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)
