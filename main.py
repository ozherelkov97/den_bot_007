from src.create_bot import bot
from src.handlers import start_message, main_menu, create_record_text, create_record_cron, delete_record


def register_handlers():
    bot.register_message_handler(start_message, commands=['start'], pass_bot=True)
    bot.register_message_handler(main_menu, content_types=['text'], pass_bot=True)
    bot.register_message_handler(create_record_text, content_types=['text'], pass_bot=True)
    bot.register_message_handler(create_record_cron, content_types=['text'], pass_bot=True)
    bot.register_message_handler(delete_record, content_types=['text'], pass_bot=True)


if __name__ == '__main__':
    register_handlers()
    bot.infinity_polling()
