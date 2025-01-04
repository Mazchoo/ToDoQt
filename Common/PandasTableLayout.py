import sys
from typing import Optional

import pandas as pd

from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow
from PyQt5.QtCore import QAbstractTableModel, Qt

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})


class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._df = data

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


class PandasTableView(QTableView):

    def __init__(self, size, parent_window):
        self.parent = parent_window
        QTableView.__init__(self, parent_window)
        self.resize(*size)
        self.clicked.connect(self.rowClick)

        self._selected_row = None

    def rowClick(self, clickedIndex):
        col = clickedIndex.column()

        if col == 0:
            row = clickedIndex.row()
            model = clickedIndex.model()
            columnsTotal = model.columnCount(None)

            for _ in range(columnsTotal):
                self.selectRow(row)

            self._selected_row = row
        else:
            self._selected_row = None

    @property
    def selected_row(self) -> Optional[int]:
        ''' If an entire row is highlighted this is the selected project '''
        return self._selected_row


if __name__ == '__main__':
    app = QApplication(sys.argv)

    parent_window = QMainWindow()
    model = PandasModel(df)

    view = PandasTableView(
        ((len(df.columns) + 1) * 127, (len(df) + 1) * 36),
        parent_window)
    view.setModel(model)
    view.showGrid()

    parent_window.show()

    sys.exit(app.exec_())