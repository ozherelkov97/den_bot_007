import telebot

menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
menu_keyboard.row('Напоминалки', 'Настройки')

records_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
records_keyboard.row('Создать', 'Удалить', 'Изменить', 'Назад')

yesno_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
yesno_keyboard.row('Да', 'Нет')