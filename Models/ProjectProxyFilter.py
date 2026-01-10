"""Class that allows a view of a model filtered by project"""

from typing import Optional

from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex


class ProjectFilterProxyModel(QSortFilterProxyModel):
    """A filtered proxy model with helper functions to filter items by project"""

    def __init__(self, model=None, filter_lambda=None, parent=None):
        super().__init__(parent)
        self.filter_lambda = filter_lambda
        self.setSourceModel(model)

    def set_filter_lambda(self, project_id: Optional[int]):
        """Set filtering function to filter for project (or for nothing when project_id is None)"""
        if project_id is not None:
            self.filter_lambda = lambda x: x.data()["project_id"] == project_id
        else:
            self.filter_lambda = None
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """Override filter function to accept row if has project id"""
        if self.filter_lambda is None:
            return False  # No filter applied, nothing to show

        ind = self.sourceModel().index(source_row, 0, source_parent)
        item = self.sourceModel().itemFromIndex(ind)

        if item is None:
            return False

        return self.filter_lambda(item)
