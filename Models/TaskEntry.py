''' Classes to create and load tasks as pydantic models '''
from typing import Tuple
from pydantic import BaseModel, field_validator

from Models import ModelParameters
from Models.FileHelpers import get_date_tuple_now


class TaskIdProvider:
    ''' Static class to update and get the latest task id '''
    max_id = 0

    @staticmethod
    def get_new_id():
        ''' Generate new task id '''
        TaskIdProvider.max_id += 1
        return TaskIdProvider.max_id

    @staticmethod
    def update_max_id(new_id):
        ''' Update id for new id that is being read '''
        TaskIdProvider.max_id = max(new_id, TaskIdProvider.max_id)


class TaskEntry(BaseModel):
    ''' Model of a loaded task '''
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
    def title_must_be_right_length(self, value):
        ''' Verify title is correct length '''
        assert len(value) <= ModelParameters.MAX_TITLE_LENGTH, 'Title too long'
        return value

    @field_validator('status')
    def status_must_be_recognised(self, value):
        ''' Verify status of task corresponds to model '''
        status_types = ModelParameters.STATUS_TYPES
        assert value in status_types, f'Status must be one of {status_types}'
        return value


def update_0_to_1(data):
    ''' Update from version 0 to 1 '''
    date_now_tuple = get_date_tuple_now()
    data['date_created'] = date_now_tuple
    data['date_edited'] = date_now_tuple


def update_1_to_2(data):
    ''' Update from version 1 to 2 '''
    date_now_tuple = get_date_tuple_now()
    data['date_moved'] = date_now_tuple
    data['id_number'] = TaskIdProvider.get_new_id()


def update_2_to_3(data):
    ''' Update from version 2 to 3 '''
    data['project_id'] = 0
    data['time_spent_seconds'] = 0
    data['estimated_time_seconds'] = 0
    data['points'] = 0


note_update_version = [
    update_0_to_1,
    update_1_to_2,
    update_2_to_3,
]


def update_task_data(task_data: dict) -> dict:
    ''' If task data needs new fields, it can update the data version '''
    if 'version' not in task_data:
        task_data['version'] = 0

    while task_data['version'] < ModelParameters.LATEST_VERSION:
        note_update_version[task_data['version']](task_data)
        task_data['version'] += 1

    return task_data


def create_new_task(item_name: str, project_id: int) -> dict:
    ''' Generate new task '''
    date_now_tuple = get_date_tuple_now()
    return {
        'title': item_name,
        'version': ModelParameters.LATEST_VERSION,
        'status': 'pending_list',
        'description': '### Summary\n\n',
        'date_created': date_now_tuple,
        'date_edited': date_now_tuple,
        'date_moved': date_now_tuple,
        'project_id': project_id,
        'time_spent_seconds': 0,
        'estimated_time_seconds': 0,
        'points': 0,
        'id_number': TaskIdProvider.get_new_id()
    }


if __name__ == '__main__':
    note_data = create_new_task('Spam', 0)
    model = TaskEntry(**note_data)
