''' Classes to create and load projects as pydantic models '''
from typing import Tuple

from pydantic import BaseModel, field_validator

from Models import ModelParameters
from Models.FileHelpers import get_date_tuple_now
from Models.IdProvider import IdProvider

PROJECT_ID_PROVIDER = IdProvider()


class Project(BaseModel):
    ''' Model of a loaded project '''
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
    @classmethod
    def title_must_be_right_length(cls, value) -> str:
        ''' Validate title '''
        assert len(value) <= ModelParameters.MAX_PROJECT_TITLE_LENGTH, 'Title too long'
        return value

    @property
    def perc_complete(self) -> float:
        ''' Percentage of hr spend versus hr remain '''
        total_hr = self.hr_spent + self.hr_remain
        if total_hr == 0.:
            return 0.
        return round(self.hr_spent / total_hr * 100, 1)

    @property
    def data_formatted(self) -> str:
        ''' Date formatted to dd/mm/yyyy '''
        year, month, day, _, _, _, _ = self.last_update
        day, month = f"0{day}"[-2:], f"0{month}"[-2:]
        return f"{day}/{month}/{year}"

    @property
    def display_dict(self) -> dict:
        ''' Get a view of the model with select fields to display '''
        field_map = ModelParameters.PROJECT_FIELDS_TO_DISPLAY
        return {v: getattr(self, k) for k, v in field_map.items()}


def create_new_project(name: str) -> dict:
    ''' Generate new project data '''
    date_now_tuple = get_date_tuple_now()
    return {
        'title': name,
        'id_number': PROJECT_ID_PROVIDER.get_new_id(),
        'version': ModelParameters.LATEST_VERSION,
        'description': '### Summary\n\n',
        'date_created': date_now_tuple,
        'last_update': date_now_tuple,
        'hr_spent': 0,
        'hr_remain': 0,
        'points_gained': 0,
    }


if __name__ == '__main__':
    project_data = create_new_project('Spam')
    model = Project(**project_data)
