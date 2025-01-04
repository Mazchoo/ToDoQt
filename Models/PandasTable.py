from typing import Self

import pandas as pd

from PyQt5.QtCore import QAbstractTableModel, Qt


class PandasModel(QAbstractTableModel):

    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self._df = data or pd.DataFrame([])

    def rowCount(self, _parent=None):
        return self._df.shape[0]

    def columnCount(self, _parent=None):
        return self._df.shape[1] + 1

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role in (Qt.EditRole, Qt.DisplayRole):
                if index.column() == 0:
                    return str(self._df.index[index.row()])
                else:
                    return str(self._df.iloc[index.row(), index.column() - 1])

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._df.iloc[index.row(), index.column() - 1] = value
            return True

    def add_row(self, row: dict) -> Self:
        self._df.loc[self.rowCount()] = pd.Series(row)
        return PandasModel(self._df)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 0:
                return "index / cols"
            else:
                return self._df.columns[col - 1]

    def flags(self, _index):
        if _index.column() != 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
