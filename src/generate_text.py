
def after_create(num):
    if num == 1:
        return f'Создал. Теперь у тебя {num} напоминалка'
    elif 2 <= num <= 3:
        return f'Создал. Теперь у тебя {num} напоминалки'
    elif num == 4:
        return f'Создал. Теперь у тебя {num} напоминалки. Не многовато?'
    elif num == 5:
        return f'Создал. Теперь у тебя {num} напоминалки. Серьезно, тебе пора поработать над памятью'
    elif num == 6:
        return f'Создал. Теперь у тебя {num} напоминалки. Как насчет поразгадывать головоломки ' \
               f'или кроссворды? Еще у меня есть контакт одного врача...'
    elif num == 7:
        return f'Создал. Теперь у тебя {num} напоминалки. Ладно, кажется это уже необратимая деменция'
    elif 8 <= num <= 20:
        return f'Создал. Теперь у тебя {num} напоминалки'
    elif num > 20 and num % 10 == 1:
        return f'Создал. Теперь у тебя {num} напоминалка'
    elif num > 7 and num % 10 in (2, 3, 4):
        return f'Создал. Теперь у тебя {num} напоминалки'
    else:
        return f'Создал. Теперь у тебя {num} напоминалок'


def after_list(records):
    first_line = "Список твоих записей:\n"
    lines = "\n".join([f"{i+1}: {r.text} ({r.cron_text})" for i, r in enumerate(records)])
    return first_line + lines


def after_delete(records):
    first_line = 'Введи номер записи, которую ты хочешь удалить:\n'
    lines = "\n".join([f"{i+1}: {r.text} ({r.cron_text})" for i, r in enumerate(records)])
    return first_line + lines
