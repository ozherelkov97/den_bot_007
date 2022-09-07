from telebot import TeleBot
from telebot.types import Message
from src.keyboards import menu_keyboard, back_keyboard
from src.utils import new_record, del_record, show_user_records_list, get_user_records_number


def start_message(message: Message, bot: TeleBot):
    msg = bot.send_message(message.chat.id, 'Приветствую тебя, забывчивый человечишко', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu, bot)


def main_menu(message: Message, bot: TeleBot):
    if message.text == 'Создать':
        msg = bot.send_message(message.chat.id, 'Отправь текст напоминалки', reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, create_record_text, bot)
    elif message.text == 'Удалить':
        reply = show_user_records_list(message.from_user.username, mode='delete')
        msg = bot.send_message(message.chat.id, reply, reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, delete_record, bot)
    elif message.text == 'Список':
        reply = show_user_records_list(message.from_user.username, mode='list')
        msg = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, main_menu, bot)


def create_record_text(message: Message, bot: TeleBot):
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, main_menu, bot)
    else:
        record_text = message.text
        msg = bot.send_message(message.chat.id, 'Как часто напоминать?')
        bot.register_next_step_handler(msg, create_record_cron, record_text, bot)


def create_record_cron(message: Message, record_text: str, bot: TeleBot,):
    reply = new_record(message, record_text)
    msg = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu, bot)


def delete_record(message: Message, bot: TeleBot):
    if message.text == 'Назад':
        return_back = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
        bot.register_next_step_handler(return_back, main_menu, bot)
    else:
        num = to_number(message, bot)
        if num is None:
            return
        if is_bad_num(message, num):
            msg = bot.send_message(message.chat.id, 'Нет такого номера', reply_markup=back_keyboard)
            bot.register_next_step_handler(msg, delete_record, bot)
            return
        reply = del_record(message, num)
        new_command = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
        bot.register_next_step_handler(new_command, main_menu, bot)


def is_bad_num(message: Message, num: int):
    return num <= 0 or num > get_user_records_number(message.from_user.username)


def to_number(message: Message, bot: TeleBot):
    try:
        num = int(message.text)
        return num
    except ValueError:
        msg = bot.send_message(message.chat.id, 'Не понял тебя. Введи номер для удаления',
                               reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, delete_record, bot)

