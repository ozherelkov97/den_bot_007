import yaml
import uuid
from data.cfg import RECORDS_PATH
import datetime


def new_record(message, text):
    record_id = uuid.uuid4().hex
    cron_text = message.text
    username = message.from_user.username
    create_dttm = datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    new_record_dict = {
        record_id: {'username': username,
                    'text': text,
                    'cron_text': cron_text,
                    'create_dttm': create_dttm
                    }
    }
    dump_new_record(new_record_dict)
    records_number = get_user_records_number(username)
    return generate_text_create(records_number)


def del_record(message, num):
    real_num = num - 1  # user inputs number from screen (and the list was shifted to start from 1, not 0
    username = message.from_user.username
    user_records = get_user_records_list(username)
    if len(user_records) == 0:
        return 'Нечего удалять'
    else:
        all_records = read_records()
        record_to_del = user_records[real_num]
        hash_to_del = get_hash(record_to_del)
        text_to_del = record_to_del['text']
        cron_text_to_del = record_to_del['cron_text']
        del all_records[hash_to_del]
        dump_all_records(all_records)
        return f'Удалил твою напоминалку №{num}: \n{text_to_del} ({cron_text_to_del})'


def dump_new_record(new_record_dict):
    with open(RECORDS_PATH, 'a', encoding='utf-8') as f:
        yaml.dump(new_record_dict, f, allow_unicode=True)


def dump_all_records(all_records_dict):
    with open(RECORDS_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(all_records_dict, f, allow_unicode=True)


def get_user_records_number(username):
    return len(get_user_records_list(username))


def show_user_records_list(username, mode='list'):
    user_records = get_user_records_list(username)
    user_records = sort_user_records_list(user_records)
    if user_records:
        if mode == 'list':
            return generate_text_list(user_records)
        elif mode == 'delete':
            return generate_text_delete(user_records)
    else:
        return 'Ты еще ничего не сохранял'


def get_user_records_list(username):
    records = read_records()
    if records:
        user_records = [r for r in records.values() if r['username'] == username]
        return sort_user_records_list(user_records)
    else:
        return []


def read_records():
    with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
        records = yaml.safe_load(f)
    return records


def sort_user_records_list(records):
    return sorted(records, key=lambda r: r['create_dttm'])


def generate_text_list(records):
    first_line = "Список твоих записей:\n"
    lines = "\n".join([f"{i+1}: {r['text']} ({r['cron_text']})" for i, r in enumerate(records)])
    return first_line + lines


def generate_text_delete(records):
    first_line = 'Введи номер записи, которую ты хочешь удалить:\n'
    lines = "\n".join([f"{i+1}: {r['text']} ({r['cron_text']})" for i, r in enumerate(records)])
    return first_line + lines


def generate_text_create(num):
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


def get_hash(record):
    records = read_records()
    return [h for h, r in records.items() if r == record][0]
