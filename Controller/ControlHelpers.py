
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


def get_selected_task(model, layout):
    if selected_item := get_selected_item_from_list(model.pending_list, layout.pending_listView):
        return selected_item
    elif selected_item := get_selected_item_from_list(model.in_progress_list, layout.inProgress_listView):
        return selected_item
    elif selected_item := get_selected_item_from_list(model.done_list, layout.done_listView):
        return selected_item
    else:
        return None


def delete_selected_task(model, layout):
    if deleted_item := delete_item_if_selected(model.pending_list, layout.pending_listView):
        return deleted_item
    elif deleted_item := delete_item_if_selected(model.in_progress_list, layout.inProgress_listView):
        return deleted_item
    elif deleted_item := delete_item_if_selected(model.done_list, layout.done_listView):
        return deleted_item
    else:
        return None
