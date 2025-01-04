
from typing import Tuple
from pydantic import BaseModel, field_validator

import Models.GlobalParams as GlobalParams
from Models.NoteFileHelpers import get_date_tuple_now


class NoteEntry(BaseModel):
    version: int
    id_number: int
    title: str
    status: str
    description: str
    project_id: int
    time_spent_seconds: int
    estimated_time_seconds: int
    points: int
    date_created: Tuple[int, int, int, int, int, int, int]
    date_edited: Tuple[int, int, int, int, int, int, int]
    date_moved: Tuple[int, int, int, int, int, int, int]

    @field_validator('title')
    def title_must_be_right_length(cls, value):
        assert len(value) <= GlobalParams.MAX_TITLE_LENGTH, 'Title too long'
        return value

    @field_validator('status')
    def status_must_be_recognised(cls, value):
        status_types = GlobalParams.STATUS_TYPES
        assert value in status_types, f'Status must be one of {status_types}'
        return value


def update_0_to_1(data):
    date_now_tuple = get_date_tuple_now()
    data['date_created'] = date_now_tuple
    data['date_edited'] = date_now_tuple


def update_1_to_2(data):
    date_now_tuple = get_date_tuple_now()
    data['date_moved'] = date_now_tuple
    data['id_number'] = GlobalParams.TaskIdProvider.get_new_id()


def update_2_to_3(data):
    data['project_id'] = 0
    data['time_spent_seconds'] = 0
    data['estimated_time_seconds'] = 0
    data['points'] = 0


note_update_version = [
    update_0_to_1,
    update_1_to_2,
    update_2_to_3,
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
        'date_moved': date_now_tuple,
        'id_number': GlobalParams.TaskIdProvider.get_new_id()
    }


if __name__ == '__main__':
    note_data = create_new_note('Spam')
    model = NoteEntry(**note_data)
