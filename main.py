from create_bot import bot
from keyboards import menu_keyboard, create_keyboard


from src.utils import new_record, generate_text_after_creation, get_user_records


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Приветствую тебя, забывчивый человечишко', reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, main_menu)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Создать':
        msg_create = bot.send_message(message.chat.id, 'Отправь текст напоминалки', reply_markup=create_keyboard)
        bot.register_next_step_handler(msg_create, create_record_text)
    elif message.text == 'Удалить':
        bot.send_message(message.chat.id, 'Я пока только напоминалки умею(', reply_markup=menu_keyboard)
    elif message.text == 'Список':
        reply = get_user_records(message.from_user.username)
        msg_create = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg_create, main_menu)


@bot.message_handler(content_types=['text'])
def create_record_text(message):
    if message.text == 'Назад':
        return_back = bot.send_message(message.chat.id, 'Назад', reply_markup=menu_keyboard)
        bot.register_next_step_handler(return_back, main_menu)
    else:
        record_text = message.text
        cron_create = bot.send_message(message.chat.id, 'Как часто напоминать?')
        bot.register_next_step_handler(cron_create, create_record_cron, record_text)


@bot.message_handler(content_types=['text'])
def create_record_cron(message, record_text):
    reply = new_record(message, record_text)
    new_command = bot.send_message(message.chat.id, reply, reply_markup=menu_keyboard)
    bot.register_next_step_handler(new_command, main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
