
from typing import Tuple

from pydantic import BaseModel, field_validator

import Models.GlobalParams as GlobalParams
from Models.FileHelpers import get_date_tuple_now

class ProjectIdProvider:
    max_id = 0

    @staticmethod
    def get_new_id():
        ProjectIdProvider.max_id += 1
        return ProjectIdProvider.max_id

    @staticmethod
    def update_max_id(new_id):
        ProjectIdProvider.max_id = max(new_id, ProjectIdProvider.max_id)


class Project(BaseModel):
    version: int
    id_number: int
    title: str
    description: str
    date_created: Tuple[int, int, int, int, int, int, int]
    last_update: Tuple[int, int, int, int, int, int, int]
    hr_spent: float
    hr_remain: float
    points_gained: int

    @field_validator('title')
    def title_must_be_right_length(cls, value):
        assert len(value) <= GlobalParams.MAX_PROJECT_TITLE_LENGTH, 'Title too long'
        return value

    @property
    def perc_complete(self) -> float:
        total_hr = self.hr_spent + self.hr_remain
        if total_hr == 0.:
            return 0.
        else:
            return round(self.hr_spent / total_hr * 100, 1)

    @property
    def data_formatted(self) -> str:
        year, month, day, _, _, _, _ = self.last_update
        day, month = f"0{day}"[-2:], f"0{month}"[-2:]
        return f"{day}/{month}/{year}"


    @property
    def display_dict(self) -> dict:
        field_map = GlobalParams.PROJECT_FIELDS_TO_DISPLAY
        return {field_map[k]: self.__getattribute__(k) for k in field_map}


def create_new_project(name: str):
    date_now_tuple = get_date_tuple_now()
    return {
        'title': name,
        'id_number': ProjectIdProvider.get_new_id(),
        'version': GlobalParams.LATEST_VERSION,
        'description': '',
        'date_created': date_now_tuple,
        'last_update': date_now_tuple,
        'hr_spent': 0,
        'hr_remain': 0,
        'points_gained': 0,
    }


if __name__ == '__main__':
    project_data = create_new_project('Spam')
    model = Project(**project_data)
