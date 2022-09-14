from telebot.types import Message
from src.records import Records

from src import generate_text


def new_record(message: Message, text: str, records: Records):
    cron_text = message.text
    username = message.from_user.username
    records.add_record(username, text, cron_text)
    records_number = records.get_user_records_number(username)
    reply_text = generate_text.after_create(records_number)
    return reply_text


def show_user_records(username: str, records: Records, mode='list'):
    user_records = sorted(records.get_user_records_list(username))
    if not user_records:
        return 'Ты еще ничего не сохранял'
    else:
        if mode == 'list':
            reply_text = generate_text.after_list(user_records)
            return reply_text
        if mode == 'delete':
            reply_text = generate_text.after_delete(user_records)
            return reply_text


def del_record(message: Message, num: int,  records: Records):
    real_num = num - 1  # user inputs number from screen (and the list was shifted to start from 1, not 0
    username = message.from_user.username
    user_records = sorted(records.get_user_records_list(username))
    if len(user_records) == 0:
        reply_text = 'Нечего удалять'
    else:
        record_to_del = user_records[real_num]
        records.delete_record(record_to_del)
        records.dump_all_records()
        reply_text = f'Удалил твою напоминалку №{num}: \n{record_to_del.text} ({record_to_del.cron_text})'
    return reply_text
