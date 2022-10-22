
from datetime import datetime
from pydantic import BaseModel, validator

# TODO consider adding global settings file

LATEST_VERSION = 1
MAX_TITLE_LENGTH = 20
STATUS_TYPES = ['pending_list', 'in_progress_list', 'done_list']

class NoteEntry(BaseModel):
    version: int = LATEST_VERSION
    title: str
    status: str
    description: str
    date_created: datetime
    
    @validator('title')
    def title_must_be_right_length(cls, value):
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError('Title too long')
        return value

    @validator('status')
    def status_must_be_recognised(cls, value):
        if value not in STATUS_TYPES:
            raise ValueError(f'Status must be one of {STATUS_TYPES}')
        return value


def update_0_to_1(data):
    data['date_created'] = datetime.now()


note_update_version = [
    update_0_to_1
]

def update_note_data(note_data: dict):
    if 'version' not in note_data:
        note_data['version'] = 0

    while note_data['version'] < LATEST_VERSION:
        note_update_version[note_data['version']](note_data)
        note_data['version'] += 1
    
    return note_data


if __name__ == '__main__':
    note_data = {
        'version': 1,
        'title': 'Noob',
        'status': 'pending_list',
        'description': 'Hello',
        'date_created': datetime.now()
    }
    model = NoteEntry(**note_data)
