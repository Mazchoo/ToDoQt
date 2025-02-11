''' Task control functions that change the state of the task models '''
from unittest.mock import MagicMock
from typing import Optional

from PyQt5.QtGui import QStandardItem

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController
from Controller.ControlHelpers import (
    append_item_to_list_view, get_selected_task, delete_selected_task,
    update_standard_item_fields, enable_time_edits, disable_time_edits,
)

from Models.TaskEntry import create_new_task, get_date_tuple_now


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def add_new_task_to_pending(self: ToDoListController, _click: bool):
    ''' If task name available and project is selected, create new task in model-view '''
    if (task_name := self.layout.newTask_lineEdit.text()) and \
       (selected_project_id := self.model.project_list.current_project_id):

        new_task = QStandardItem(task_name)
        new_task.setData(create_new_task(task_name, selected_project_id))
        new_task.setAccessibleDescription(new_task.data()["description"])

        append_item_to_list_view(self.model.pending_list, self.model.pending_filter,
                                 self.layout.pending_listView, new_task)
        self.layout.newTask_lineEdit.setText("")
        self.layout.addNewTask_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def select_current_task(self: ToDoListController, selected_task: Optional[QStandardItem]):
    ''' Set-up GUI for a selecting a task '''
    if selected_task is None:
        return

    self.layout.taskDescription_textEdit.setText(selected_task.accessibleDescription())
    self.layout.taskDescription_textEdit.setEnabled(True)
    self.task_description_handler.render_markdown()
    self.layout.deleteTask_pushButton.setEnabled(True)
    self.layout.saveTaskChanges_pushButton.setEnabled(False)

    enable_time_edits(self, selected_task)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def delete_current_task(self: ToDoListController, _click: bool):
    ''' Delete current task if selected '''
    if delete_selected_task(self.model, self.layout):
        self.layout.taskDescription_textEdit.setText("")
        self.layout.backup_pushButton.setEnabled(True)

        if not get_selected_task(self.model, self.layout):
            self.layout.deleteTask_pushButton.setEnabled(False)

        self.recalculate_current_project()
        disable_time_edits(self)


@ClassMethod(ToDoListController)
@QtControlFunction()
def check_enable_task_save_changes(self: ToDoListController):
    ''' Check if task changes should be enabled if description has changed '''
    if (selected_task := get_selected_task(self.model, self.layout)) and self.task_description_handler.is_editing:
        old_description = selected_task.accessibleDescription()
        description_changed = self.layout.taskDescription_textEdit.toPlainText() != old_description
        self.layout.saveTaskChanges_pushButton.setEnabled(description_changed)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_add_new_task(self: ToDoListController):
    ''' If new task title not empty, enable add new task '''
    new_task_title_empty = self.layout.newTask_lineEdit.displayText() == ''
    self.layout.addNewTask_pushButton.setEnabled(not new_task_title_empty)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_current_task_description(self: ToDoListController, _click: bool):
    ''' Save current description to model from task description text edit '''
    if selected_task := get_selected_task(self.model, self.layout):
        description = self.task_description_handler.raw_markdown
        selected_task.setAccessibleDescription(description)
        update_fields = {'description': selected_task.accessibleDescription(),
                         'date_edited': get_date_tuple_now()}
        update_standard_item_fields(selected_task, **update_fields)

        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction()
def task_title_changed(self: ToDoListController):
    ''' Update task model if title changed '''
    if selected_task := get_selected_task(self.model, self.layout):
        new_title = selected_task.text()
        if new_title != selected_task.data()["title"]:
            update_fields = {"title": selected_task.text()}
            update_standard_item_fields(selected_task, **update_fields)
            self.layout.backup_pushButton.setEnabled(True)
