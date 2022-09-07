from dataclasses import dataclass, asdict
from datetime import datetime
from telebot.types import Message

import yaml


@dataclass(frozen=True, order=True)
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
        dict_to_dump = asdict(new_record)
        with open(self.path, 'a', encoding='utf-8') as f:
            yaml.dump(dict_to_dump, f, allow_unicode=True)


reminders_list = []
with open('data/records.yml', 'r', encoding='utf-8') as f:
    file_dict = yaml.safe_load(f)

for h, r in file_dict.items():
    next_reminder = SingleRecord(**r)
    print(next_reminder.__hash__())
    print(next_reminder)
    print(asdict(next_reminder))
    reminders_list.append(next_reminder)

records = Records(reminders_list)
print(records.get_user_records_number('ozherelkov'))
