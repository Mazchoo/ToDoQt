import sys
from typing import Optional, List

import pandas as pd

from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow
from Models.PandasTable import PandasModel

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})


class PandasTableView(QTableView):

    def __init__(self, parent_window):
        self.parent = parent_window
        super().__init__(parent_window)

        self.clicked.connect(self.rowClick)

        self._selected_row = None

    def adjust_size(self, nr_rows, row_height, col_widths):
        self.set_column_widths(col_widths)
        self.set_row_heights(nr_rows, row_height)
        self.resize(sum(col_widths), (nr_rows + 1) * row_height)

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

    def set_column_widths(self, widths: List[int]):
        for i, width in enumerate(widths):
            self.setColumnWidth(i, width)

    def set_row_heights(self, nr_rows: int, height: int):
        self.horizontalHeader().setFixedHeight(height) 
        for i in range(nr_rows):
            self.setRowHeight(i, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    parent_window = QMainWindow()
    model = PandasModel(df)

    view = PandasTableView(parent_window)
    view.setModel(model)

    model = model.add_row({'a': 'Bob', 'b': 400, 'c': 'd'})
    view.setModel(model)
    view.adjust_size(model.rowCount(), 36, [100, 100, 100, 100])

    parent_window.show()

    sys.exit(app.exec_())
