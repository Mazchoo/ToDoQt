
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

def list_view_has_selected_item(list_view: QListView):
    return True if list_view.selectedIndexes() else False


def get_selected_item_from_list(model_list: QStandardItemModel, list_view: QListView):
    selected_indices = list_view.selectedIndexes()
    if selected_indices:
        return model_list.item(selected_indices[0].row())


def delete_item_if_selected(model_list: QStandardItemModel, list_view: QListView):
    selected_indices = list_view.selectedIndexes()
    if selected_indices:
        deleted_item = model_list.takeRow(selected_indices[0].row())[0]
        list_view.setModel(model_list)
        return deleted_item


def append_item_to_list_view(model_list: QStandardItemModel, list_view: QListView, standard_item: QStandardItem):
    if not standard_item: return
    model_list.appendRow(standard_item)
    list_view.setModel(model_list)
    return standard_item
