
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction
from Controller.Controller import ToDoListController


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


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def delete_current_item(self, _click):
    deleted_item = delete_item_if_selected(self.model.pending_list, self.layout.pending_listView)
    if deleted_item is None:
        deleted_item = delete_item_if_selected(self.model.in_progress_list, self.layout.inProgress_listView)
    if deleted_item is None:
        deleted_item = delete_item_if_selected(self.model.done_list, self.layout.done_listView)

    if deleted_item:
        self.layout.description_textEdit.setText("")


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def add_name_to_list(self, _click: bool):
    if item_name := self.layout.newTask_lineEdit.text():
        standard_item = QStandardItem(item_name)
        append_item_to_list_view(self.model.pending_list, self.layout.pending_listView, standard_item)
        self.layout.newTask_lineEdit.setText("")


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_pendingView(self, _click: bool):
    self.layout.inProgress_listView.clearSelection()
    self.layout.done_listView.clearSelection()
    selected_item = get_selected_item_from_list(self.model.pending_list, self.layout.pending_listView)
    self.layout.description_textEdit.setText(selected_item.accessibleDescription())


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_in_progressView(self, _click: bool):
    self.layout.pending_listView.clearSelection()
    self.layout.done_listView.clearSelection()
    selected_item = get_selected_item_from_list(self.model.in_progress_list, self.layout.inProgress_listView)
    self.layout.description_textEdit.setText(selected_item.accessibleDescription())


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_doneView(self, _click: bool):
    self.layout.inProgress_listView.clearSelection()
    self.layout.pending_listView.clearSelection()
    selected_item = get_selected_item_from_list(self.model.done_list, self.layout.done_listView)
    self.layout.description_textEdit.setText(selected_item.accessibleDescription())


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setCurrentTask_to_pending(self, _click: bool):
    if item_taken := delete_item_if_selected(self.model.in_progress_list, self.layout.inProgress_listView):
        return append_item_to_list_view(self.model.pending_list, self.layout.pending_listView, item_taken)
    if item_taken := delete_item_if_selected(self.model.done_list, self.layout.done_listView):
        return append_item_to_list_view(self.model.pending_list, self.layout.pending_listView, item_taken)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setCurrentTask_to_inProgress(self, _click: bool):
    if item_taken := delete_item_if_selected(self.model.pending_list, self.layout.pending_listView):
        return append_item_to_list_view(self.model.in_progress_list, self.layout.inProgress_listView, item_taken)
    if item_taken := delete_item_if_selected(self.model.done_list, self.layout.done_listView):
        return append_item_to_list_view(self.model.in_progress_list, self.layout.inProgress_listView, item_taken)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setCurrentTask_to_done(self, _click: bool):
    if item_taken := delete_item_if_selected(self.model.pending_list, self.layout.pending_listView):
        return append_item_to_list_view(self.model.done_list, self.layout.done_listView, item_taken)
    if item_taken := delete_item_if_selected(self.model.in_progress_list, self.layout.inProgress_listView):
        return append_item_to_list_view(self.model.done_list, self.layout.done_listView, item_taken)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_current_item_description(self, _click: bool):
    selected_item = get_selected_item_from_list(self.model.pending_list, self.layout.pending_listView)
    if selected_item is None:
        selected_item = get_selected_item_from_list(self.model.in_progress_list, self.layout.inProgress_listView)
    if selected_item is None:
        selected_item = get_selected_item_from_list(self.model.done_list, self.layout.done_listView)

    if selected_item:
        selected_item.setAccessibleDescription(self.layout.description_textEdit.toPlainText())


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_backups(self, _click: bool):
    self.model.save_to_folder("SavedToDo")
