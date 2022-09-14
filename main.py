from src.create_bot import bot
from src.handlers import start_message, main_menu, create_record_first_handler, \
    create_record_second_handler, delete_record_handler


def register_handlers():
    bot.register_message_handler(start_message, commands=['start'], pass_bot=True)
    bot.register_message_handler(main_menu, content_types=['text'], pass_bot=True)
    bot.register_message_handler(create_record_first_handler, content_types=['text'], pass_bot=True)
    bot.register_message_handler(create_record_second_handler, content_types=['text'], pass_bot=True)
    bot.register_message_handler(delete_record_handler, content_types=['text'], pass_bot=True)


if __name__ == '__main__':
    register_handlers()
    bot.infinity_polling()
