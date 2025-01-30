''' Model to handle project table '''
from typing import Self, Optional, List, Tuple, Union

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal, QModelIndex

from Models.ModelParameters import PROJECT_FIELDS_TO_DISPLAY
from Models.ProjectEntry import Project
from UI.DisplayParameters import (PROJECT_TABLE_LEFT_ALGIN_COLUMNS,
                                  PROJECT_TABLE_EDITABLE_COLUMNS)


class ProjectTableModel(QAbstractTableModel):
    ''' Table model specialised for handling project data from a stored dataframe '''
    dataUpdated = pyqtSignal()  # Custom signal

    def __init__(self, data: Optional[List[Project]] = None):
        QAbstractTableModel.__init__(self)

        # These data containers intended to be private and immutable (changing underling data is okay)
        self._data = data or []
        display_data = [project.display_dict for project in self._data]
        self._df = pd.DataFrame(display_data, columns=PROJECT_FIELDS_TO_DISPLAY.values())

        self._selected_row = None

    @property
    def selected_row(self) -> Optional[int]:
        ''' Currently selected row (set from other class), is None when no row selected '''
        return self._selected_row

    def set_selected_row(self, ind: Optional[int]):
        ''' Set currently selected row '''
        self._selected_row = ind

    def rowCount(self, _parent=None):
        ''' Get number of rows from underlying '''
        return self._df.shape[0]

    def columnCount(self, _parent=None):
        ''' Get number of columns from underlying dataframe (including index column) '''
        return self._df.shape[1] + 1

    def data(self, ind: QModelIndex, role=Qt.DisplayRole) -> Union[Qt.AlignmentFlag, str, None]:
        ''' Getter function to display data from underlying dataframe '''
        if ind.isValid():
            if role in (Qt.EditRole, Qt.DisplayRole):
                if ind.column() == 0:
                    return str(self._df.index[ind.row()])
                return str(self._df.iloc[ind.row(), ind.column() - 1])

            if role == Qt.TextAlignmentRole:
                # Alignment should be left center vertical by default
                if ind.column() not in PROJECT_TABLE_LEFT_ALGIN_COLUMNS:
                    return Qt.AlignCenter
        return None

    def setData(self, ind: QModelIndex, value: str, role: int) -> bool:
        ''' Update model override updates underlying dataframe '''
        if role == Qt.EditRole and self._df.iloc[ind.row(), ind.column() - 1] != value and ind.isValid():
            self._df.iloc[ind.row(), ind.column() - 1] = value
            inverse_map = {v: k for k, v in PROJECT_FIELDS_TO_DISPLAY.items()}
            field_name = inverse_map[self._df.columns[ind.column() - 1]]
            setattr(self._data[ind.row()], field_name, value)
            self.dataUpdated.emit()
            return True
        return False

    def headerData(self, col: int, orientation: Qt.Orientation, role: int) -> Optional[str]:
        ''' Override to get column name '''
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 0:
                return "Id"
            return self._df.columns[col - 1]
        return None

    def flags(self, ind: QModelIndex) -> Qt.ItemFlags:
        ''' Allow items in editable column to be edited '''
        if ind.column() in PROJECT_TABLE_EDITABLE_COLUMNS:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def add_project(self, project: Project) -> Self:
        ''' Get mutated table with extra project added '''
        return ProjectTableModel(self._data + [project])

    def delete_selected_project(self) -> Optional[Self]:
        ''' Get mutated table with selected row removed, return None on invalid selected row '''
        if self._selected_row is None or self._selected_row >= len(self._data):
            return None

        new_data = self._data.copy()
        new_data.pop(self._selected_row)
        return ProjectTableModel(new_data)

    @property
    def current_description(self) -> str:
        ''' Get description of current selected row or empty string on invalid row '''
        if self._selected_row is None or self._selected_row >= len(self._data):
            return ""
        return self._data[self._selected_row].description

    def set_current_description(self, description: str) -> bool:
        ''' Set the description of the current selected row '''
        if self._selected_row is None or self._selected_row >= len(self._data):
            return False
        self._data[self._selected_row].description = description
        return True

    @property
    def current_project_id(self) -> Optional[int]:
        ''' Get current selected projected or None on invalid selected row '''
        if self._selected_row is None or self._selected_row >= len(self._data):
            return None
        return self._data[self._selected_row].id_number

    @property
    def save_dump(self) -> List[dict]:
        ''' Serialize table as list of dictionaries '''
        return [project.model_dump() for project in self._data]

    def _update_data_with_id(self, project_id: int, **kwargs) -> Optional[Tuple[int, Project]]:
        ''' Private function to update project with id with kwargs '''
        for i, project in enumerate(self._data):
            if project.id_number == project_id:
                for key, value in kwargs.items():
                    setattr(project, key, value)
                return (i, project)
        return None

    def update_project_data(self, project_id: int, **kwargs):
        ''' Update project data and display with project id '''
        if row_id_project := self._update_data_with_id(project_id, **kwargs):
            i, project = row_id_project
            self._df.iloc[i] = project.display_dict
