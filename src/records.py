from dataclasses import dataclass, asdict
from datetime import datetime
import yaml


@dataclass(frozen=True, unsafe_hash=True, order=True)
class SingleRecord:
    create_dttm: datetime
    username: str
    text: str
    cron_text: str


class Records:
    def __init__(self, records_list: list, path='data/records.yml'):
        self.records = records_list
        self.path = path

    def get_user_records_list(self, username):
        return [rec for rec in self.records if rec.username == username]

    def get_user_records_number(self, username):
        return len(self.get_user_records_list(username))

    def add_record(self, username: str, text: str, cron_text: str):
        new_record = SingleRecord(create_dttm=datetime.now(),
                                  username=username,
                                  text=text,
                                  cron_text=cron_text)
        self.records.append(new_record)
        self.dump_new_record(new_record)

    def delete_record(self, record: SingleRecord):
        index = hash(record)
        del self.records[index]

    def dump_new_record(self, new_record: SingleRecord):
        dict_to_dump = {hash(new_record): asdict(new_record)}
        with open(self.path, 'a', encoding='utf-8') as f:
            yaml.dump(dict_to_dump, f, allow_unicode=True)

    def dump_all_records(self):
        with open(self.path, 'a', encoding='utf-8') as f:
            for rec in self.records:
                yaml.dump({hash(rec): asdict(rec)}, f, allow_unicode=True)


def update_records(path: str):
    reminders_list = []
    with open(path, 'r', encoding='utf-8') as f:
        file_dict = yaml.safe_load(f)
    for h, r in file_dict.items():
        next_reminder = SingleRecord(**r)
        reminders_list.append(next_reminder)
    return Records(reminders_list)
