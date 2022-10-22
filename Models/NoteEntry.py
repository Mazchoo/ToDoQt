
from typing import Tuple
from datetime import datetime
from pydantic import BaseModel, validator

import Models.GlobalParams as GlobalParams

class NoteEntry(BaseModel):
    version: int = GlobalParams.LATEST_VERSION
    title: str
    status: str
    description: str
    date_created: Tuple[int, int, int, int, int, int, int]
    date_edited: Tuple[int, int, int, int, int, int, int]
    
    @validator('title')
    def title_must_be_right_length(cls, value):
        assert len(value) <= GlobalParams.MAX_TITLE_LENGTH, 'Title too long'
        return value

    @validator('status')
    def status_must_be_recognised(cls, value):
        status_types = GlobalParams.STATUS_TYPES
        assert value in status_types, f'Status must be one of {status_types}'
        return value

def get_date_tuple_now():
    return eval(repr(datetime.now())[17:])


def update_0_to_1(data):
    date_now_tuple = get_date_tuple_now()
    data['date_created'] = date_now_tuple
    data['date_edited'] = date_now_tuple


note_update_version = [
    update_0_to_1
]

def update_note_data(note_data: dict):
    if 'version' not in note_data:
        note_data['version'] = 0

    while note_data['version'] < GlobalParams.LATEST_VERSION:
        note_update_version[note_data['version']](note_data)
        note_data['version'] += 1
    
    return note_data


def create_new_note(item_name: str):
    date_now_tuple = get_date_tuple_now()
    return {
        'title': item_name,
        'version': GlobalParams.LATEST_VERSION,
        'status': 'pending_list',
        'description': '',
        'date_created': date_now_tuple,
        'date_edited': date_now_tuple,
    }


if __name__ == '__main__':
    note_data = create_new_note('Spam')
    model = NoteEntry(**note_data)
