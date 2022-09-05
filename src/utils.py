import yaml
import uuid
from data.cfg import RECORDS_PATH


def new_record(message, record_text):
    record_id = uuid.uuid4().hex
    cron_text = message.text
    username = message.from_user.username
    new_record_dict = {
        record_id: {'username': username,
                    'record_text': record_text,
                    'cron_text': cron_text}
    }
    dump_record(new_record_dict)
    records_number = get_user_records_number(username)
    return generate_text_after_creation(records_number)


def dump_record(new_record_dict):
    with open(RECORDS_PATH, 'a', encoding='utf-8') as f:
        yaml.dump(new_record_dict, f, allow_unicode=True)


def get_user_records_number(username):
    with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
        records = yaml.safe_load(f)
    return sum([r['username'] == username for r in records.values()])


def generate_text_after_creation(num):
    if num == 1:
        return f'Создал. Теперь у тебя {num} заметка'
    elif 2 <= num <= 3:
        return f'Создал. Теперь у тебя {num} заметки'
    elif num == 4:
        return f'Создал. Теперь у тебя {num} заметки. Не многовато?'
    elif num == 5:
        return f'Создал. Теперь у тебя {num} заметок. Серьезно, тебе пора поработать над памятью'
    elif num == 6:
        return f'Создал. Теперь у тебя {num} заметок. Как насчет поразгадывать головоломки ' \
               f'или кроссворды? Еще у меня есть контакт одного врача...'
    elif num == 7:
        return f'Создал. Теперь у тебя {num} заметок. Ладно, кажется это уже необратимая деменция'
    elif 8 <= num <= 20:
        return f'Создал. Теперь у тебя {num} заметок'
    elif num > 20 and num % 10 == 1:
        return f'Создал. Теперь у тебя {num} заметка'
    elif num > 7 and num % 10 in (2, 3, 4):
        return f'Создал. Теперь у тебя {num} заметки'
    else:
        return f'Создал. Теперь у тебя {num} заметок'


def get_user_records(username):
    with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
        records = yaml.safe_load(f)
    user_records = [(r['record_text'], r['cron_text']) for r in records.values() if r['username'] == username]
    return generate_text_for_list(user_records)


def generate_text_for_list(user_records):
    return '\n'.join([f'{record_text} ({cron_text})' for (record_text, cron_text) in user_records])
