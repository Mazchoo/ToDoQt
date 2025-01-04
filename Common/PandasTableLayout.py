import sys
from typing import Optional

import pandas as pd

from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow
from Models.PandasTable import PandasModel


df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})


class PandasTableView(QTableView):

    def __init__(self, rows, cols, parent_window):
        self.parent = parent_window
        QTableView.__init__(self, parent_window)
        self.adjust_size(rows, cols)
        self.clicked.connect(self.rowClick)

        self._selected_row = None

    def adjust_size(self, rows, cols):
        self.resize((cols + 1) * 127, (rows + 1) * 36)

    def rowClick(self, clicked_index):
        col = clicked_index.column()

        if col == 0:
            row = clicked_index.row()
            model = clicked_index.model()
            columnsTotal = model.columnCount()

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

    view = PandasTableView(len(df), len(df.columns), parent_window)
    view.setModel(model)
    view.showGrid()

    model = model.add_row({'a': 'Bob', 'b': 400, 'c': 'd'})
    view.setModel(model)
    view.adjust_size(len(df), len(df.columns))

    parent_window.show()

    sys.exit(app.exec_())
