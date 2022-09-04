from create_bot import bot
import yaml

from handlers.message_handlers import start_message, main_menu

# with open('data/records.yml', 'r') as f:
#     records = yaml.safe_load(f)

if __name__ == '__main__':
    bot.polling(none_stop=True)
