
from PyQt5.QtGui import QStandardItem

from unittest.mock import MagicMock

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController
from Controller.UploadGitThread import UPLOAD_THREAD_SINGLETON
from Controller.ControlHelpers import (
    get_selected_item_from_list, append_item_to_list_view,
    get_selected_task, delete_selected_task, update_standard_item_fields
)
from Models.NoteEntry import create_new_note, get_date_tuple_now


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def delete_current_item(self, _click):
    if delete_selected_task(self.model, self.layout):
        self.layout.description_textEdit.setText("")
        self.layout.backup_pushButton.setEnabled(True)

        if not get_selected_task(self.model, self.layout):
            self.layout.delete_pushButton.setEnabled(False)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def add_name_to_list(self, _click: bool):
    if item_name := self.layout.newTask_lineEdit.text():
        standard_item = QStandardItem(item_name)
        standard_item.setData(create_new_note(item_name))

        append_item_to_list_view(self.model.pending_list, self.layout.pending_listView, standard_item)
        self.layout.newTask_lineEdit.setText("")
        self.layout.addNewTask_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def set_text_description(self, selected_item: QStandardItem):
    if selected_item is None:
        return

    self.layout.description_textEdit.setText(selected_item.accessibleDescription())
    self.layout.delete_pushButton.setEnabled(True)
    self.layout.saveChanges_pushButton.setEnabled(False)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_pendingView(self, _click: bool):
    self.layout.inProgress_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_item = get_selected_item_from_list(self.model.pending_list, self.layout.pending_listView)
    set_text_description(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_in_progressView(self, _click: bool):
    self.layout.pending_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_item = get_selected_item_from_list(self.model.in_progress_list, self.layout.inProgress_listView)
    set_text_description(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_doneView(self, _click: bool):
    self.layout.inProgress_listView.clearSelection()
    self.layout.pending_listView.clearSelection()

    selected_item = get_selected_item_from_list(self.model.done_list, self.layout.done_listView)
    set_text_description(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_current_item_description(self, _click: bool):
    if selected_item := get_selected_task(self.model, self.layout):
        selected_item.setAccessibleDescription(self.layout.description_textEdit.toPlainText())
        update_fields = {'description': selected_item.accessibleDescription(),
                         'date_edited': get_date_tuple_now()}
        selected_item = update_standard_item_fields(selected_item, **update_fields)

        self.layout.saveChanges_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_backups(self, _click: bool):
    self.model.save_to_folder("SavedToDo")
    self.layout.backup_pushButton.setEnabled(False)
    self.layout.upload_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def close_window(self, _click: bool):
    self.parent.close()


@ClassMethod(ToDoListController)
def stop_animation(self):
    self.layout.loaderAnimation_label.setVisible(False)
    UPLOAD_THREAD_SINGLETON.running = False
    UPLOAD_THREAD_SINGLETON.finished.disconnect()


@ClassMethod(ToDoListController)
def start_upload(self):
    self.layout.loaderAnimation_label.setVisible(True)
    UPLOAD_THREAD_SINGLETON.running = True
    UPLOAD_THREAD_SINGLETON.started.disconnect()


@ClassMethod(ToDoListController)
def git_push_backups(self, _click: bool):
    if not UPLOAD_THREAD_SINGLETON.running:
        self.layout.upload_pushButton.setEnabled(False)
        UPLOAD_THREAD_SINGLETON.finished.connect(self.stop_animation)
        UPLOAD_THREAD_SINGLETON.started.connect(self.start_upload)
        UPLOAD_THREAD_SINGLETON.start()


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_save_changes(self):
    if selected_item := get_selected_task(self.model, self.layout):
        old_description = selected_item.accessibleDescription()
        description_changed = self.layout.description_textEdit.toPlainText() != old_description
        self.layout.saveChanges_pushButton.setEnabled(description_changed)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_add_new_item(self):
    new_task_empty = self.layout.newTask_lineEdit.displayText() == ''
    self.layout.addNewTask_pushButton.setEnabled(not new_task_empty)
