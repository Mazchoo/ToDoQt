from typing import Self, Optional, List, Tuple

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal

from Models.ModelParameters import PROJECT_FIELDS_TO_DISPLAY
from Models.ProjectEntry import Project
from UI.DisplayParameters import (PROJECT_TABLE_LEFT_ALGIN_COLUMNS,
                                  PROJECT_TABLE_EDITABLE_COLUMNS)


class ProjectTableModel(QAbstractTableModel):

    dataUpdated = pyqtSignal() 

    def __init__(self, data: Optional[List[Project]] = None):
        QAbstractTableModel.__init__(self)

        # These data containers intended to be private and immutable (changing underling data is okay)
        self._data = data or []
        display_data = [project.display_dict for project in self._data]
        self._df = pd.DataFrame(display_data, columns=PROJECT_FIELDS_TO_DISPLAY.values())

        self._selected_row = None

    @property
    def selected_row(self) -> Optional[int]:
        return self._selected_row

    def set_selected_row(self, ind: Optional[int]):
        self._selected_row = ind

    def rowCount(self, _parent=None):
        return self._df.shape[0]

    def columnCount(self, _parent=None):
        return self._df.shape[1] + 1

    def data(self, ind, role=Qt.DisplayRole):
        if ind.isValid():
            if role in (Qt.EditRole, Qt.DisplayRole):
                if ind.column() == 0:
                    return str(self._df.index[ind.row()])
                else:
                    return str(self._df.iloc[ind.row(), ind.column() - 1])
            if role == Qt.TextAlignmentRole:
                # Alignment should be left center vertical by default
                if ind.column() not in PROJECT_TABLE_LEFT_ALGIN_COLUMNS:
                    return Qt.AlignCenter

    def setData(self, ind, value, role):
        if role == Qt.EditRole and self._df.iloc[ind.row(), ind.column() - 1] != value:
            self._df.iloc[ind.row(), ind.column() - 1] = value
            # Assume deterministic dictionary order
            field_name = list(PROJECT_FIELDS_TO_DISPLAY.keys())[ind.column() - 1]
            self._data[ind.row()].__setattr__(field_name, value)
            self.dataUpdated.emit()
            return True
        return False

    def add_project(self, project: Project) -> Self:
        return ProjectTableModel(self._data + [project])

    def delete_selected_project(self) -> Optional[Self]:
        if self._selected_row is None or self._selected_row >= len(self._data):
            return None

        new_data = self._data.copy()
        new_data.pop(self._selected_row)
        return ProjectTableModel(new_data)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 0:
                return "Id"
            else:
                return self._df.columns[col - 1]

    def flags(self, ind):
        if ind.column() in PROJECT_TABLE_EDITABLE_COLUMNS:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    @property
    def current_description(self) -> str:
        if self._selected_row is None or self._selected_row >= len(self._data):
            return ""
        return self._data[self._selected_row].description

    def set_current_description(self, description: str) -> bool:
        if self._selected_row is None or self._selected_row >= len(self._data):
            return False
        self._data[self._selected_row].description = description
        return True

    @property
    def current_project_id(self) -> Optional[int]:
        if self._selected_row is None or self._selected_row >= len(self._data):
            return None
        return self._data[self._selected_row].id_number

    @property
    def save_dump(self) -> List[dict]:
        return [project.model_dump() for project in self._data]

    def _update_data_with_id(self, project_id: Project, **kwargs) -> Optional[Tuple[int, Project]]:
        for i, project in enumerate(self._data):
            if project.id_number == project_id:
                for key, value in kwargs.items():
                    setattr(project, key, value)
                return (i, project)
        return None

    def update_project_data(self, project_id: int, **kwargs):
        if row_id_project := self._update_data_with_id(project_id, **kwargs):
            i, project = row_id_project
            self._df.iloc[i] = project.display_dict
