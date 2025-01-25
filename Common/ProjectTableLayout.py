import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow, QAbstractItemView
from Models.ProjectTable import ProjectTableModel


class ProjectTableView(QTableView):

    def __init__(self, parent_window, max_height: int):
        self.parent = parent_window
        self.max_height = max_height
        super().__init__(parent_window)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def adjust_size(self, nr_rows, row_height, col_widths):
        self.set_column_widths(col_widths)
        self.set_row_heights(nr_rows, row_height)
        self.resize(sum(col_widths), min((nr_rows + 1) * row_height, self.max_height))

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
    model = ProjectTableModel()

    view = ProjectTableView(parent_window, 500)

    view.setModel(model)
    view.adjust_size(model.rowCount(), 50, [100, 100, 100, 100, 25])

    parent_window.show()

    sys.exit(app.exec_())
