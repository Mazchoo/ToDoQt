
from unittest.mock import MagicMock
from typing import Optional

from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import QTime

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController
from Controller.UploadGitThread import UPLOAD_THREAD_SINGLETON
from Controller.ControlHelpers import (
    get_selected_item_from_list, append_item_to_list_view, get_selected_task,
    delete_selected_task, update_standard_item_fields, not_uploaded_changes_present,
    update_pandas_table_in_layout, filter_available_tasks_for_selected_project,
    get_seconds_from_qt_time, enable_time_edits, disable_time_edits,
    recalculate_hours_spent, recalculate_hours_remain, recalculate_total_points,
    execute_layout_change
)

from Models.TaskEntry import create_new_note, get_date_tuple_now
from Models.ProjectEntry import Project, create_new_project


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def delete_current_item(self, _click):
    if delete_selected_task(self.model, self.layout):
        self.layout.taskDescription_textEdit.setText("")
        self.layout.backup_pushButton.setEnabled(True)

        if not get_selected_task(self.model, self.layout):
            self.layout.deleteTask_pushButton.setEnabled(False)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def add_new_task_to_pending(self, _click: bool):
    if (task_name := self.layout.newTask_lineEdit.text()) and \
       (selected_project_id := self.model.project_list.current_project_id):

        new_task = QStandardItem(task_name)
        new_task.setData(create_new_note(task_name, selected_project_id))

        append_item_to_list_view(self.model.pending_list, self.model.pending_filter,
                                 self.layout.pending_listView, new_task)
        self.layout.newTask_lineEdit.setText("")
        self.layout.addNewTask_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def add_new_project(self, _click: bool):
    if project_name := self.layout.newProject_lineEdit.text():
        new_project = Project(**create_new_project(project_name))
        self.model.project_list = self.model.project_list.add_project(new_project)
        update_pandas_table_in_layout(self.layout.project_tableView, self.model.project_list)

        self.layout.addNewProject_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def select_current_task(self, selected_item: Optional[QStandardItem]):
    if selected_item is None:
        return

    self.layout.taskDescription_textEdit.setText(selected_item.accessibleDescription())
    self.layout.deleteTask_pushButton.setEnabled(True)
    self.layout.saveTaskChanges_pushButton.setEnabled(False)

    enable_time_edits(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_pendingView(self, _click: bool):
    self.layout.inProgress_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_item = get_selected_item_from_list(self.model.pending_list, self.model.pending_filter,
                                                self.layout.pending_listView)
    select_current_task(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_in_progressView(self, _click: bool):
    self.layout.pending_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_item = get_selected_item_from_list(self.model.in_progress_list, self.model.in_progress_filter,
                                                self.layout.inProgress_listView)
    select_current_task(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_doneView(self, _click: bool):
    self.layout.inProgress_listView.clearSelection()
    self.layout.pending_listView.clearSelection()

    selected_item = get_selected_item_from_list(self.model.done_list, self.model.done_filter,
                                                self.layout.done_listView)
    select_current_task(self, selected_item)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_current_task_description(self, _click: bool):
    if selected_item := get_selected_task(self.model, self.layout):
        selected_item.setAccessibleDescription(self.layout.taskDescription_textEdit.toPlainText())
        update_fields = {'description': selected_item.accessibleDescription(),
                         'date_edited': get_date_tuple_now()}
        update_standard_item_fields(selected_item, **update_fields)

        self.layout.saveTaskChanges_pushButton.setEnabled(False)
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
def end_upload(self):
    self.layout.loaderAnimation_label.setVisible(False)
    UPLOAD_THREAD_SINGLETON.running = False
    UPLOAD_THREAD_SINGLETON.finished.disconnect()
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())


@ClassMethod(ToDoListController)
def start_upload(self):
    self.layout.loaderAnimation_label.setVisible(True)
    UPLOAD_THREAD_SINGLETON.running = True
    UPLOAD_THREAD_SINGLETON.started.disconnect()


@ClassMethod(ToDoListController)
def git_push_backups(self, _click: bool):
    if not UPLOAD_THREAD_SINGLETON.running:
        self.layout.upload_pushButton.setEnabled(False)
        UPLOAD_THREAD_SINGLETON.finished.connect(self.end_upload)
        UPLOAD_THREAD_SINGLETON.started.connect(self.start_upload)
        UPLOAD_THREAD_SINGLETON.start()


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_task_save_changes(self):
    if selected_item := get_selected_task(self.model, self.layout):
        old_description = selected_item.accessibleDescription()
        description_changed = self.layout.taskDescription_textEdit.toPlainText() != old_description
        self.layout.saveTaskChanges_pushButton.setEnabled(description_changed)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_add_new_task(self):
    new_task_empty = self.layout.newTask_lineEdit.displayText() == ''
    self.layout.addNewTask_pushButton.setEnabled(not new_task_empty)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_add_new_project(self):
    new_task_empty = self.layout.newProject_lineEdit.displayText() == ''
    self.layout.addNewProject_pushButton.setEnabled(not new_task_empty)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_upload_if_uncomitted_changes(self):
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def project_row_click(self, clicked_index):
    prev_project_id = self.model.project_list.current_project_id
    row = clicked_index.row()
    self.model.project_list.set_selected_row(row)
    project_id = self.model.project_list.current_project_id

    if project_id != prev_project_id:
        filter_available_tasks_for_selected_project(self.model, project_id)

        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.deleteTask_pushButton.setEnabled(False)
        self.layout.taskDescription_textEdit.setText("")
        disable_time_edits(self)

        self.layout.deleteProject_pushButton.setEnabled(True)
        text_descrition = self.model.project_list.current_description
        self.layout.projectDescription_textEdit.setText(text_descrition)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def project_header_click(self, _clicked_index):
    self.model.project_list.set_selected_row(None)
    filter_available_tasks_for_selected_project(self.model, None)

    self.layout.saveTaskChanges_pushButton.setEnabled(False)
    self.layout.deleteTask_pushButton.setEnabled(False)
    self.layout.taskDescription_textEdit.setText("")
    disable_time_edits(self)

    self.layout.project_tableView.clearSelection()
    self.layout.deleteProject_pushButton.setEnabled(False)
    self.layout.projectDescription_textEdit.setText("")


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_project_save_if_text_changed(self):
    if self.model.project_list.selected_row:
        old_description = self.model.project_list.current_description
        description_changed = self.layout.projectDescription_textEdit.toPlainText() != old_description
        self.layout.saveProjectChanges_pushButton.setEnabled(description_changed)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_project_save(self):
    self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_current_project_description(self, _click: bool):
    if self.model.project_list.selected_row:
        description = self.layout.projectDescription_textEdit.toPlainText()
        self.model.project_list.set_current_description(description)

        self.layout.saveProjectChanges_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def edit_time_spent_spinner(self, time: QTime):
    if selected_item := get_selected_task(self.model, self.layout):
        total_seconds = get_seconds_from_qt_time(time)
        update_standard_item_fields(selected_item, time_spent_seconds=total_seconds)
        self.layout.backup_pushButton.setEnabled(True)
        recalculate_current_project(self)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def edit_time_estimate_spinner(self, time: QTime):
    if selected_item := get_selected_task(self.model, self.layout):
        total_seconds = get_seconds_from_qt_time(time)
        update_standard_item_fields(selected_item, estimated_time_seconds=total_seconds)
        self.layout.backup_pushButton.setEnabled(True)
        recalculate_current_project(self)


@ClassMethod(ToDoListController)
@QtControlFunction(0.)
def edit_points_spinner(self, value: int):
    if selected_item := get_selected_task(self.model, self.layout):
        update_standard_item_fields(selected_item, points=value)
        self.layout.backup_pushButton.setEnabled(True)
        recalculate_current_project(self)


@ClassMethod(ToDoListController)
@QtControlFunction()
def recalculate_current_project(self):
    if project_id := self.model.project_list.current_project_id:
        with execute_layout_change(self.model.project_list):
            update_dict = {
                "hr_spent": round(recalculate_hours_spent(self.model, project_id), 1),
                "hr_remain": round(recalculate_hours_remain(self.model, project_id), 1),
                "points_gained": recalculate_total_points(self.model, project_id)
            }
            self.model.project_list.update_project_data(project_id, **update_dict)


@ClassMethod(ToDoListController)
@QtControlFunction()
def update_current_project_date(self):
    if project_id := self.model.project_list.current_project_id:
        with execute_layout_change(self.model.project_list):
            update_dict = {
                "last_update": get_date_tuple_now(),
            }
            self.model.project_list.update_project_data(project_id, **update_dict)


@ClassMethod(ToDoListController)
@QtControlFunction()
def delete_current_project(self, _click: bool):
    if new_project_list := self.model.project_list.delete_selected_project():
        self.model.project_list = new_project_list
        update_pandas_table_in_layout(self.layout.project_tableView, self.model.project_list)

        self.layout.backup_pushButton.setEnabled(True)
        self.layout.deleteProject_pushButton.setEnabled(False)
