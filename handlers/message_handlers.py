from create_bot import bot
from keyboards import menu_keyboard, create_keyboard
import yaml
import uuid


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Приветствую тебя, забывчивый человечишко', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Создать':
        msg_create = bot.send_message(message.chat.id, 'Отправь текст напоминалки', reply_markup=create_keyboard)
        bot.register_next_step_handler(msg_create, create_record)

    elif message.text == 'Удалить':
        bot.send_message(message.chat.id, 'Я пока только напоминалки умею(', reply_markup=menu_keyboard)
    elif message.text == 'Список':
        bot.send_message(message.chat.id, 'Я пока только напоминалки умею(', reply_markup=menu_keyboard)


@bot.message_handler(content_types=['text'])
def create_record(message):
    if message.text == 'Назад':
        return_back = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
        bot.register_next_step_handler(return_back, main_menu)
    else:
        record_text = message.text
        cron_create = bot.send_message(message.chat.id, 'Как часто напоминать?', reply_markup=create_keyboard)
        bot.register_next_step_handler(cron_create, cron_for_record, record_text)


@bot.message_handler(content_types=['text'])
def cron_for_record(message, record_text):
    cron_text = message.text
    record_id = uuid.uuid4().hex
    new_record = {record_id: {'username': message.from_user.username,
                              'record_text': record_text,
                              'cron_text': cron_text}}
    with open('data/records.yml', 'a', encoding='utf-8') as outfile:
        yaml.dump(new_record, outfile, allow_unicode=True)

    new_command = bot.send_message(message.chat.id, 'Ок, создали', reply_markup=menu_keyboard)
    bot.register_next_step_handler(new_command, main_menu)
