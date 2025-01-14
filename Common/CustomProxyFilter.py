from PyQt5.QtCore import Qt, QSortFilterProxyModel

class CustomFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, model=None, filter_lambda=None, parent=None):
        super().__init__(parent)
        self.filter_lambda = filter_lambda
        self.setSourceModel(model)

    def setFilterLambda(self, filter_lambda):
        self.filter_lambda = filter_lambda
        self.invalidateFilter()  # Refresh the filter

    def filterAcceptsRow(self, source_row, source_parent):
        if self.filter_lambda is None:
            return True  # No filter applied, nothing to show

        # Access the data from the source model
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        data = source_model.data(index, Qt.DisplayRole)

        # Apply the lambda function to decide whether to include this row
        return self.filter_lambda(data)
