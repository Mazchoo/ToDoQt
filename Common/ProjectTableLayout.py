"""View of project table"""

import sys
from typing import List, Optional

from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow, QAbstractItemView
from Models.ProjectTable import ProjectTableModel
from Models.ProjectProxyFilter import ProjectFilterProxyModel


class ProjectTableView(QTableView):
    """Table with resizing properties for project view"""

    def __init__(self, parent_window: QMainWindow, max_height: int):
        self.parent = parent_window
        self.max_height = max_height
        self._source_model: Optional[ProjectTableModel] = None
        self._proxy_model = ProjectFilterProxyModel()
        super().__init__(parent_window)
        super().setModel(self._proxy_model)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # pylint: disable=no-member

    @property
    def is_showing_archive(self) -> bool:
        """Return true if showing archive"""
        return self._proxy_model.show_archived

    def setModel(self, model: ProjectTableModel):
        """Override setModel to use proxy model for filtering"""
        self._source_model = model
        self._proxy_model.setSourceModel(model)

    def toggle_show_archive(self) -> bool:
        """Set whether to show archived projects and refresh the view"""
        return self._proxy_model.toggle_show_archive()

    def adjust_size(self, nr_rows: int, row_height: int, col_widths: List[int]):
        """Ajust table size"""
        self.set_column_widths(col_widths)
        # Use proxy model row count for sizing
        visible_rows = self._proxy_model.rowCount() if self._proxy_model else nr_rows
        self.set_row_heights(visible_rows, row_height)
        self.resize(
            sum(col_widths), min((visible_rows + 1) * row_height, self.max_height)
        )

    def get_source_row(self, proxy_row: int) -> Optional[int]:
        """Get the source model row index from proxy row index"""
        if self._proxy_model:
            proxy_index = self._proxy_model.index(proxy_row, 0)
            source_index = self._proxy_model.mapToSource(proxy_index)
            return source_index.row()
        return proxy_row

    def set_column_widths(self, widths: List[int]):
        """Set widths of columns"""
        for i, width in enumerate(widths):
            self.setColumnWidth(i, width)

    def set_row_heights(self, nr_rows: int, height: int):
        """Set heights of all rows"""
        self.horizontalHeader().setFixedHeight(height)
        for i in range(nr_rows):
            self.setRowHeight(i, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    parent = QMainWindow()
    project_model = ProjectTableModel()

    view = ProjectTableView(parent, 500)

    view.setModel(project_model)
    view.adjust_size(project_model.rowCount(), 50, [100, 100, 100, 100, 25])

    parent.show()

    sys.exit(app.exec_())
