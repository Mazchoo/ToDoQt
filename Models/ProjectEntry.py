
from typing import Tuple
from pydantic import BaseModel, field_validator

import Models.GlobalParams as GlobalParams
from Models.FileHelpers import get_date_tuple_now


class Project(BaseModel):
    version: int
    id_number: int
    title: str
    description: str
    date_created: Tuple[int, int, int, int, int, int, int]
    date_last_worked_on: Tuple[int, int, int, int, int, int, int]

    @field_validator('title')
    def title_must_be_right_length(cls, value):
        assert len(value) <= GlobalParams.MAX_TITLE_LENGTH, 'Title too long'
        return value


def create_new_project(item_name: str):
    date_now_tuple = get_date_tuple_now()
    return {
        'title': item_name,
        'version': GlobalParams.LATEST_VERSION,
        'description': '',
        'date_created': date_now_tuple,
        'date_last_worked_on': date_now_tuple,
        'id_number': GlobalParams.ProjectIdProvider.get_new_id()
    }


if __name__ == '__main__':
    project_data = create_new_project('Spam')
    model = Project(**project_data)
