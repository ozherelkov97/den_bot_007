from telebot import TeleBot
from telebot.types import Message
from src.keyboards import menu_keyboard, back_keyboard
from src.utils import new_record, del_record, show_user_records
from src.records import Records, update_records

from data.cfg import RECORDS_PATH


def start_message(message: Message, bot: TeleBot):
    msg = bot.send_message(message.chat.id, 'Приветствую тебя, забывчивый человечишко', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu, bot)


def main_menu(message: Message, bot: TeleBot):
    if message.text == 'Создать':
        records = update_records(RECORDS_PATH)
        msg = bot.send_message(message.chat.id, 'Отправь текст напоминалки', reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, create_record_first_handler, bot, records)
    elif message.text == 'Удалить':
        records = update_records(RECORDS_PATH)
        reply = show_user_records(message.from_user.username, records, mode='delete')
        msg = bot.send_message(message.chat.id, reply, reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, delete_record_handler, bot, records)
    elif message.text == 'Список':
        records = update_records(RECORDS_PATH)
        reply = show_user_records(message.from_user.username, records, mode='list')
        msg = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, main_menu, bot, records)


def create_record_first_handler(message: Message, bot: TeleBot, records: Records):
    if message.text == 'Назад':
        back_to_main(message, bot, records)
    else:
        record_text = message.text
        msg = bot.send_message(message.chat.id, 'Как часто напоминать?')
        bot.register_next_step_handler(msg, create_record_second_handler, record_text, bot, records)


def create_record_second_handler(message: Message, record_text: str, bot: TeleBot, records: Records):
    reply = new_record(message, record_text, records)
    msg = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu, bot, records)


def delete_record_handler(message: Message, bot: TeleBot, records: Records):
    if message.text == 'Назад':
        back_to_main(message, bot, records)
    else:
        num = to_number(message, bot, records)
        if num is None:
            return
        if is_bad_num(message, num, records):
            msg = bot.send_message(message.chat.id, 'Нет такого номера', reply_markup=back_keyboard)
            bot.register_next_step_handler(msg, delete_record_handler, bot, records)
            return
        reply = del_record(message, num, records)
        new_command = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
        bot.register_next_step_handler(new_command, main_menu, bot, records)


def is_bad_num(message: Message, num: int, records: Records):
    return num <= 0 or num > records.get_user_records_number(message.from_user.username)


def to_number(message: Message, bot: TeleBot, records: Records):
    try:
        num = int(message.text)
        return num
    except ValueError:
        msg = bot.send_message(message.chat.id, 'Не понял тебя. Введи номер для удаления',
                               reply_markup=back_keyboard)
        bot.register_next_step_handler(msg, delete_record_handler, bot, records)


def back_to_main(message: Message, bot: TeleBot, records: Records):
    msg = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu, bot, records)
