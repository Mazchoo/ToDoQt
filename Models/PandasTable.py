from typing import Self

import pandas as pd

from PyQt5.QtCore import QAbstractTableModel, Qt
from Models.GlobalParams import PROJECT_FIELDS_TO_DISPLAY
from UI.DisplayParameters import (PROJECT_TABLE_LEFT_ALGIN_COLUMNS,
                                  PROJECT_TABLE_EDITABLE_COLUMNS)


class PandasModel(QAbstractTableModel):

    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        if data is not None:
            self._df = data
        else:
            self._df = pd.DataFrame([], columns=PROJECT_FIELDS_TO_DISPLAY.values())

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

    def add_row(self, row: dict) -> Self:
        self._df.loc[self.rowCount()] = pd.Series(row)
        return PandasModel(self._df)

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

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()
