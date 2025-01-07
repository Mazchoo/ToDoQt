from typing import Self, Optional, List

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt

from Models.GlobalParams import PROJECT_FIELDS_TO_DISPLAY
from Models.ProjectEntry import Project
from UI.DisplayParameters import (PROJECT_TABLE_LEFT_ALGIN_COLUMNS,
                                  PROJECT_TABLE_EDITABLE_COLUMNS)


class PandasModel(QAbstractTableModel):

    def __init__(self, data: Optional[List[Project]] = None):
        QAbstractTableModel.__init__(self)
        self._data = data or []

        display_data = [project.display_dict for project in self._data]
        self._df = pd.DataFrame(display_data, columns=PROJECT_FIELDS_TO_DISPLAY.values())

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
        if role == Qt.EditRole:
            self._df.iloc[ind.row(), ind.column() - 1] = value
            return True

    def add_project(self, project: Project) -> Self:
        return PandasModel(self._data + [project])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 0:
                return "Index"
            else:
                return self._df.columns[col - 1]

    def flags(self, ind):
        if ind.column() in PROJECT_TABLE_EDITABLE_COLUMNS:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def get_description_at_ind(self, ind: Optional[int]) -> str:
        if ind is None or ind >= len(self._data):
            return ""
        return self._data[ind].description

    def set_description_at_ind(self, ind: Optional[int], description: str) -> bool:
        if ind is None or ind >= len(self._data):
            return False
        self._data[ind].description = description
        return True

    @property
    def save_dump(self) -> List[dict]:
        return [project.model_dump() for project in self._data]
