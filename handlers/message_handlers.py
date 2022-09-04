from create_bot import bot
from keyboards import menu_keyboard, records_keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Приветствую', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu)


# @bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Напоминалки':
        action = bot.send_message(message.chat.id, 'Что хочешь с ними сделать?', reply_markup=menu_keyboard)
        bot.register_next_step_handler(action, main_menu)
    elif message.text == 'Настройки':
        bot.send_message(message.chat.id, 'Я пока только напоминалки умею(', reply_markup=menu_keyboard)
    elif message.text == 'Настройки':
        bot.send_message(message.chat.id, '', reply_markup=menu_keyboard)
