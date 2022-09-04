import telebot
import mysql.connector

friendly_db = mysql.connector.connect(
  host="localhost",
  user="root",
  # password="up",
  database="friendly_db"
)
#hello
mycursor = friendly_db.cursor()

# mycursor.execute("CREATE DATABASE h")
# mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE, name VARCHAR(255))")
# mycursor.execute("CREATE TABLE notes (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, created_dttm DATETIME, "
#                  "text VARCHAR(255), valid_from_dttm DATETIME, valid_to_dttm DATETIME, del_flg INT)")

# sql = "INSERT INTO users (user_id, name) VALUES (%s, %s)"
# val = (667, "Highway to Hell")
# mycursor.execute(sql, val)
# friendly_db.commit()


bot = telebot.TeleBot('1022063217:AAFgKDtMgCNzfN86LZUUOUVfEJYPkYUknnE')


menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
menu_keyboard.row('Заметки', 'Не заметки', 'Настройки')

notes_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
notes_keyboard.row('Посмотреть', 'Написать', 'Удалить', 'Изменить', 'Назад')

yesno_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
yesno_keyboard.row('Да', 'Нет')

notes = []


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    sql = "SELECT name from users WHERE user_id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()

    if len(result):
        msg = bot.send_message(message.chat.id, 'Приветствую', reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, menu)
    else:
        msg = bot.send_message(message.chat.id, 'Привет, я помогу тебе, брат. Как тебя зовут?')
        bot.register_next_step_handler(msg, get_name)


def get_name(message):
    name = message.text
    msg = bot.send_message(message.chat.id, 'То есть мне называть тебя ' + name + '?', reply_markup=yesno_keyboard)
    bot.register_next_step_handler(msg, lambda m: confirm_name(m, name))


def confirm_name(message, name):
    if message.text == 'Да':
        user_id = message.from_user.id
        sql = "SELECT name from users WHERE user_id = %s"
        val = (user_id, )
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if len(result):
            msg = bot.send_message(message.chat.id,
                                   'Вы уже зарегистрированы под именем ' + result[0][0] + '. Хотите сменить имя?',
                                   reply_markup=yesno_keyboard)
            bot.register_next_step_handler(msg, lambda m: ask_change_name(m, name))

        else:
            sql = "INSERT INTO users (user_id, name) VALUES (%s, %s)"
            val = (user_id, name)
            mycursor.execute(sql, val)
            friendly_db.commit()
            if name != message.from_user.first_name:
                msg = bot.send_message(message.chat.id, 'Павел Дуров считает, что на самом деле вас зовут ' +
                                       message.from_user.first_name + ', но и так сойдет)', reply_markup=menu_keyboard)
                bot.register_next_step_handler(msg, menu)
            else:
                msg = bot.send_message(message.chat.id, 'Ну и имечко у тебя))', reply_markup=menu_keyboard)
                bot.register_next_step_handler(msg, menu)
    else:
        msg = bot.send_message(message.chat.id, 'Тогда как?')
        bot.register_next_step_handler(msg, get_name)


def ask_change_name(message, name):
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, 'На какое? На ' + name + '?', reply_markup=yesno_keyboard)
        bot.register_next_step_handler(msg, lambda m: change_name(m, name))
    else:
        msg = bot.send_message(message.chat.id, 'Ок', reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, menu)


def change_name(message, name):
    if message.text == 'Да':
        sql = "UPDATE users SET name = %s WHERE user_id = %s"
        val = (name, int(message.from_user.id))
        mycursor.execute(sql, val)
        friendly_db.commit()
        msg = bot.send_message(message.chat.id, 'Сменил', reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, menu)
    else:
        msg = bot.send_message(message.chat.id, 'Ок', reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, menu)


@bot.message_handler(content_types=['text'])
def settings(message):
    if message.text == 'Заметки':
        action = bot.send_message(message.chat.id, 'Что хочешь с ними сделать?', reply_markup=notes_keyboard)
        bot.register_next_step_handler(action, note)
    elif message.text == 'Не заметки':
        bot.send_message(message.chat.id, 'Я пока только заметки умею(', reply_markup=menu_keyboard)


@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Заметки':
        action = bot.send_message(message.chat.id, 'Что хочешь с ними сделать?', reply_markup=notes_keyboard)
        bot.register_next_step_handler(action, note)
    elif message.text == 'Не заметки':
        bot.send_message(message.chat.id, 'Я пока только заметки умею(', reply_markup=menu_keyboard)
    elif message.text == 'Настройки':
        bot.send_message(message.chat.id, '', reply_markup=menu_keyboard)


@bot.message_handler(content_types=['text'])
def note(message):
    if message.text == 'Посмотреть':
        if len(notes) > 0:
            list_of_notes = '\n'.join(['[' + str(i + 1) + '] ' + record for i, record in enumerate(notes)])
            msg = bot.send_message(message.chat.id, list_of_notes, reply_markup=notes_keyboard)
            bot.register_next_step_handler(msg, note)
            return
        else:
            msg = bot.send_message(message.chat.id, 'Ты их не написал, братишка', reply_markup=notes_keyboard)
            bot.register_next_step_handler(msg, note)
            return
    elif message.text == 'Написать':
        answer = bot.send_message(message.chat.id, 'Напиши заметку)')
        bot.register_next_step_handler(answer, write_note)
        return
    elif message.text == 'Удалить':
        if len(notes) > 0:
            bot.send_message(message.chat.id, 'Напиши, заметку с каким номером ты хочешь удалить:')
            list_of_notes = '\n'.join(['[' + str(i+1) + '] ' + record for i, record in enumerate(notes)])
            answer = bot.send_message(message.chat.id, list_of_notes)
            bot.register_next_step_handler(answer, delete_note)
            return
        else:
            answer = bot.send_message(message.chat.id, 'У тебя же нет заметок, чудила)', reply_markup=notes_keyboard)
            bot.register_next_step_handler(answer, note)
            return
    elif message.text == 'Изменить':
        if len(notes) > 0:
            bot.send_message(message.chat.id, 'Напиши, заметку с каким номером ты хочешь изменить:')
            list_of_notes = '\n'.join(['[' + str(i+1) + '] ' + record for i, record in enumerate(notes)])
            answer = bot.send_message(message.chat.id, list_of_notes)
            bot.register_next_step_handler(answer, change_note)
            return
        else:
            answer = bot.send_message(message.chat.id, 'Нет заметок у тебя!', reply_markup=notes_keyboard)
            bot.register_next_step_handler(answer, note)
            return
    elif message.text == 'Назад':
        action = bot.send_message(message.chat.id, 'Возвращаемся в меню', reply_markup=menu_keyboard)
        bot.register_next_step_handler(action, menu)
    else:
        action = bot.send_message(message.chat.id, 'Чего? Команду выбери', reply_markup=notes_keyboard)
        bot.register_next_step_handler(action, note)


@bot.message_handler(content_types=['text'])
def write_note(message):
    notes.append(message.text)
    response = 'теперь заметок у тебя: ' + str(len(notes))
    msg = bot.send_message(message.chat.id, response, reply_markup=notes_keyboard)
    bot.register_next_step_handler(msg, note)
    return


@bot.message_handler(content_types=['text'])
def delete_note(message):
    # Проверка, что введено число
    is_number = True
    try:
        num = int(message.text)
    except ValueError:
        is_number = False

    # Если не было ValueError, то удаляем заметку с этим номером, иначе переспрашиваем
    if is_number:
        if 1 <= num <= len(notes):
            notes.pop(num-1)
            response = 'теперь заметок у тебя: ' + str(len(notes))
            msg = bot.send_message(message.chat.id, response, reply_markup=notes_keyboard)
            bot.register_next_step_handler(msg, note)
            return
        else:
            msg = bot.send_message(message.chat.id, 'Нет такой, мб все-таки другую?')
            bot.register_next_step_handler(msg, delete_note)
            return
    else:
        msg = bot.send_message(message.chat.id, 'Не понял, какой номер заметки?')
        bot.register_next_step_handler(msg, delete_note)
        return


def change_note(message):
    # Проверка, что введено число
    is_number = True
    try:
        num = int(message.text)
    except ValueError:
        is_number = False

    # Если не было ValueError, то изменяем заметку с этим номером, иначе переспрашиваем
    if is_number:
        if 1 <= num <= len(notes):
            msg = bot.send_message(message.chat.id, 'Заметка: \n' + notes[num-1] + '\n Редактируй:')
            bot.register_next_step_handler(msg, lambda m: change_note_finally(m, num))
            return
        else:
            msg = bot.send_message(message.chat.id, 'Нет такой, мб все-таки другую?')
            bot.register_next_step_handler(msg, change_note)
            return
    else:
        msg = bot.send_message(message.chat.id, 'Номер это типа число, введи его')
        bot.register_next_step_handler(msg, change_note)
        return


def change_note_finally(msg, num):
    notes[num - 1] = msg.text
    msg = bot.send_message(msg.chat.id, 'Заметка отредактирована)', reply_markup=notes_keyboard)
    bot.register_next_step_handler(msg, note)
    return


bot.polling()
