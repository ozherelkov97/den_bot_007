from create_bot import bot
from keyboards import menu_keyboard, back_keyboard

from src.utils import new_record, del_record, show_user_records_list, get_user_records_number


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Приветствую тебя, забывчивый человечишко', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Создать':
        msg = bot.send_message(message.chat.id, 'Отправь текст напоминалки', reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, create_record_text)
    elif message.text == 'Удалить':
        reply = show_user_records_list(message.from_user.username, mode='delete')
        msg = bot.send_message(message.chat.id, reply, reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, delete_record)
    elif message.text == 'Список':
        reply = show_user_records_list(message.from_user.username, mode='list')
        msg = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, main_menu)


@bot.message_handler(content_types=['text'])
def create_record_text(message):
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, main_menu)
    else:
        record_text = message.text
        msg = bot.send_message(message.chat.id, 'Как часто напоминать?')
        bot.register_next_step_handler(msg, create_record_cron, record_text)


@bot.message_handler(content_types=['text'])
def create_record_cron(message, record_text):
    reply = new_record(message, record_text)
    msg = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu)


@bot.message_handler(content_types=['text'])
def delete_record(message):
    if message.text == 'Назад':
        return_back = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
        bot.register_next_step_handler(return_back, main_menu)
    else:
        try:
            num = int(message.text)
            if num <= 0 or num > get_user_records_number(message.from_user.username):
                msg = bot.send_message(message.chat.id, 'Нет такого номера', reply_markup=back_keyboard)
                bot.register_next_step_handler(msg, delete_record)
            else:
                reply = del_record(message, num)
                new_command = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
                bot.register_next_step_handler(new_command, main_menu)
        except ValueError:
            msg = bot.send_message(message.chat.id, 'Не понял тебя. Введи номер для удаления',
                                   reply_markup=back_keyboard)
            bot.register_next_step_handler(msg, delete_record)


if __name__ == '__main__':
    bot.polling(none_stop=True)
