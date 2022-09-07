import telebot

menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
menu_keyboard.row('Создать', 'Удалить', 'Список')

back_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
back_keyboard.row('Назад')

yesno_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
yesno_keyboard.row('Да', 'Нет')
