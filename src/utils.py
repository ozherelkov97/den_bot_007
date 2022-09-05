import yaml
import uuid
from data.cfg import RECORDS_PATH


def new_record(message, record_text):
    record_id = uuid.uuid4().hex
    cron_text = message.text
    username = message.from_user.username
    records_num = get_user_records_number(username)
    new_record_dict = {
        record_id: {'num': records_num + 1,
                    'username': username,
                    'record_text': record_text,
                    'cron_text': cron_text}
    }
    dump_new_record(new_record_dict)
    records_number = get_user_records_number(username)
    return generate_text_create(records_number)


def del_record(message, num):
    username = message.from_user.username
    if get_user_records_number == 0:
        return 'Нечего удалять'
    else:
        with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
            records = yaml.safe_load(f)
        hash_to_del = [h for h, r in records.items() if r['username'] == username and r['num'] == num][0]
        record_text_to_del = records[hash_to_del]['record_text']
        cron_text_to_del = records[hash_to_del]['cron_text']
        del records[hash_to_del]
        dump_all_records(records)
        return f'Удалил твою напоминалку №{num} ({record_text_to_del}, {cron_text_to_del})'


def dump_new_record(new_record_dict):
    with open(RECORDS_PATH, 'a', encoding='utf-8') as f:
        yaml.dump(new_record_dict, f, allow_unicode=True)


def dump_all_records(all_records_dict):
    with open(RECORDS_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(all_records_dict, f, allow_unicode=True)


def get_user_records_number(username):
    return len(get_user_records_list(username))


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


def show_user_records_list(username, mode='list'):
    records = get_user_records_list(username)
    if records:
        if mode == 'list':
            return generate_text_list(records)
        elif mode == 'delete':
            return generate_text_delete(records)
    else:
        return 'Ты еще ничего не сохранял'


def get_user_records_list(username):
    with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
        records = yaml.safe_load(f)
    if records:
        return [r for r in records.values() if r['username'] == username]
    else:
        return []


def generate_text_list(records):
    first_line = "Список твоих записей:\n"
    lines = "\n".join([f"{r['num']}: {r['record_text']} ({r['cron_text']})" for r in records])
    return first_line + lines


def generate_text_delete(records):
    first_line = 'Введи номер записи, которую ты хочешь удалить:\n'
    lines = "\n".join([f"{r['num']}: {r['record_text']} ({r['cron_text']})" for r in records])
    return first_line + lines


# def get_hash_by_username_num(username, num):
#     with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
#         records = yaml.safe_load(f)
#     return [h for h, r in records.items() if r['username'] == username and r['num'] == num][0]
