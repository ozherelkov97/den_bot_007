from dataclasses import dataclass, asdict
from datetime import datetime

import yaml


@dataclass(frozen=True, order=True)
class SingleRecord:
    create_dttm: datetime
    username: str
    text: str
    cron_text: str


class Records:
    def __init__(self, records_list: list):
        self.records = records_list

    def get_user_records_list(self, username):
        return [rec for rec in self.records if rec.username == username]

    def get_user_records_number(self, username):
        return len(self.get_user_records_list(username))


reminders_list = []
with open('data/records.yml', 'r', encoding='utf-8') as f:
    file_dict = yaml.safe_load(f)

for h, r in file_dict.items():
    next_reminder = SingleRecord(**r)
    reminders_list.append(next_reminder)

records = Records(reminders_list)
print(records.get_user_records_number('ozherelkov'))
