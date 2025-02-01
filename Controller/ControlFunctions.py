''' Functions that change state of the GUI '''
from unittest.mock import MagicMock
from typing import Optional

from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import QTime, QModelIndex

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction
from Common.QtHelpers import loadQss

from Controller.Controller import ToDoListController
from Controller.UploadGitThread import UPLOAD_THREAD_SINGLETON
from Controller.ControlHelpers import (
    get_selected_item_from_list, append_item_to_list_view, get_selected_task,
    delete_selected_task, update_standard_item_fields, not_uploaded_changes_present,
    update_pandas_table_in_layout, filter_available_tasks_for_selected_project,
    get_seconds_from_qt_time, enable_time_edits, disable_time_edits,
    recalculate_hours_spent, recalculate_hours_remain, recalculate_total_points,
    execute_layout_change, delete_all_items_with_project_id,
    get_default_hour_to_points_valuation
)

from Models.TaskEntry import create_new_task, get_date_tuple_now
from Models.ProjectEntry import Project, create_new_project


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
@QtControlFunction(True)
def add_new_project(self: ToDoListController, _click: bool):
    ''' Add new project if project name is available '''
    if project_name := self.layout.newProject_lineEdit.text():
        try:
            new_project = Project(**create_new_project(project_name))
        except ValueError as e:
            print(f"New project is invalid schema with error {e}")
            return

        self.model.project_list = self.model.project_list.add_project(new_project)
        update_pandas_table_in_layout(self.layout.project_tableView, self.model.project_list)

        self.layout.newProject_lineEdit.setText("")
        self.layout.addNewProject_pushButton.setEnabled(False)
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
def setFocus_to_pendingView(self: ToDoListController, _click: bool):
    ''' Set-up GUI for pending view '''
    self.layout.inProgress_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_task = get_selected_item_from_list(self.model.pending_list, self.model.pending_filter,
                                                self.layout.pending_listView)
    select_current_task(self, selected_task)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_in_progressView(self: ToDoListController, _click: bool):
    ''' Set-up GUI for in progress view '''
    self.layout.pending_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_task = get_selected_item_from_list(self.model.in_progress_list, self.model.in_progress_filter,
                                                self.layout.inProgress_listView)
    select_current_task(self, selected_task)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_doneView(self: ToDoListController, _click: bool):
    ''' Set-up GUI for in done view '''
    self.layout.inProgress_listView.clearSelection()
    self.layout.pending_listView.clearSelection()

    selected_task = get_selected_item_from_list(self.model.done_list, self.model.done_filter,
                                                self.layout.done_listView)
    select_current_task(self, selected_task)


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
@QtControlFunction(True)
def save_backups(self: ToDoListController, _click: bool):
    ''' Save all model data to folder '''
    self.model.save_to_folder("SavedToDo")
    self.layout.backup_pushButton.setEnabled(False)
    self.layout.upload_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def close_window(self: ToDoListController, _click: bool):
    ''' Close window action '''
    self.parent.close()


@ClassMethod(ToDoListController)
def end_upload(self: ToDoListController):
    ''' Set-up GUI for finishing upload '''
    self.layout.loaderAnimation_label.setVisible(False)
    UPLOAD_THREAD_SINGLETON.running = False
    UPLOAD_THREAD_SINGLETON.finished.disconnect()
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())


@ClassMethod(ToDoListController)
def start_upload(self: ToDoListController):
    ''' Set-up GUI for starting upload '''
    self.layout.loaderAnimation_label.setVisible(True)
    UPLOAD_THREAD_SINGLETON.running = True
    UPLOAD_THREAD_SINGLETON.started.disconnect()


@ClassMethod(ToDoListController)
def git_push_backups(self: ToDoListController, _click: bool):
    ''' Save backups in repo '''
    if not UPLOAD_THREAD_SINGLETON.running:
        self.layout.upload_pushButton.setEnabled(False)
        UPLOAD_THREAD_SINGLETON.finished.connect(self.end_upload)
        UPLOAD_THREAD_SINGLETON.started.connect(self.start_upload)
        UPLOAD_THREAD_SINGLETON.start()


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
@QtControlFunction()
def enable_add_new_project(self: ToDoListController):
    ''' If new project title not empty, enable add new task '''
    new_project_title_empty = self.layout.newProject_lineEdit.displayText() == ''
    self.layout.addNewProject_pushButton.setEnabled(not new_project_title_empty)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_upload_if_uncomitted_changes(self: ToDoListController):
    ''' Enable upload if changes unuploaded changes present '''
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def project_row_click(self: ToDoListController, clicked_index: QModelIndex):
    ''' Reset GUI for clicking on a project '''
    prev_project_id = self.model.project_list.current_project_id
    row = clicked_index.row()
    self.model.project_list.set_selected_row(row)
    project_id = self.model.project_list.current_project_id
    self.project_description_handler.stop_editing()

    if project_id != prev_project_id:
        filter_available_tasks_for_selected_project(self.model, project_id)

        self.layout.newTask_lineEdit.setEnabled(True)
        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.deleteTask_pushButton.setEnabled(False)
        self.layout.taskDescription_textEdit.setText("")
        self.layout.taskDescription_textEdit.setEnabled(False)
        disable_time_edits(self)

        self.layout.saveProjectChanges_pushButton.setEnabled(False)

        self.layout.deleteProject_pushButton.setEnabled(True)
        self.layout.projectDescription_textEdit.setEnabled(True)
        text_descrition = self.model.project_list.current_description
        self.layout.projectDescription_textEdit.setText(text_descrition)
        self.project_description_handler.render_markdown()


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def project_header_click(self: ToDoListController, _clicked_index: QModelIndex):
    ''' Remove project selection '''
    self.model.project_list.set_selected_row(None)
    filter_available_tasks_for_selected_project(self.model, None)

    self.layout.newTask_lineEdit.setText("")
    self.layout.newTask_lineEdit.setEnabled(False)
    self.layout.saveTaskChanges_pushButton.setEnabled(False)
    self.layout.deleteTask_pushButton.setEnabled(False)
    self.layout.taskDescription_textEdit.setText("")
    self.layout.taskDescription_textEdit.setEnabled(False)
    disable_time_edits(self)

    self.layout.project_tableView.clearSelection()
    self.layout.deleteProject_pushButton.setEnabled(False)
    self.layout.projectDescription_textEdit.setText("")
    self.layout.projectDescription_textEdit.setEnabled(False)


@ClassMethod(ToDoListController)
@QtControlFunction()
def check_enable_project_save(self: ToDoListController):
    ''' If project description changed, enable save project changes '''
    if self.model.project_list.selected_row is not None and self.project_description_handler.is_editing:
        old_description = self.model.project_list.current_description
        description_changed = self.layout.projectDescription_textEdit.toPlainText() != old_description
        self.layout.saveProjectChanges_pushButton.setEnabled(description_changed)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_project_save(self: ToDoListController):
    ''' Enable project save button '''
    self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_current_project_description(self: ToDoListController, _click: bool):
    ''' Update project model with new description '''
    if self.model.project_list.selected_row is not None:
        description = self.project_description_handler.raw_markdown
        self.model.project_list.set_current_description(description)

        self.layout.saveProjectChanges_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(QTime(0, 0, 0))
def edit_time_spent_spinner(self: ToDoListController, time: QTime):
    ''' Recalculate project stats on time spent edit '''
    if selected_task := get_selected_task(self.model, self.layout):
        total_seconds = get_seconds_from_qt_time(time)
        update_standard_item_fields(selected_task, time_spent_seconds=total_seconds)
        self.layout.backup_pushButton.setEnabled(True)
        update_current_project_date(self)
        self.recalculate_current_project()


@ClassMethod(ToDoListController)
@QtControlFunction(QTime(0, 0, 0))
def edit_time_estimate_spinner(self: ToDoListController, time: QTime):
    ''' Recalculate project stats on time estimate edit '''
    if selected_task := get_selected_task(self.model, self.layout):
        total_seconds = get_seconds_from_qt_time(time)
        points = get_default_hour_to_points_valuation(self, selected_task, total_seconds)

        update_standard_item_fields(selected_task, estimated_time_seconds=total_seconds, points=points)
        self.layout.backup_pushButton.setEnabled(True)
        self.recalculate_current_project()


@ClassMethod(ToDoListController)
@QtControlFunction(0.)
def edit_points_spinner(self: ToDoListController, value: int):
    ''' Recalculate project stats on points edit '''
    if selected_task := get_selected_task(self.model, self.layout):
        update_standard_item_fields(selected_task, points=value)
        self.layout.backup_pushButton.setEnabled(True)
        self.recalculate_current_project()


@ClassMethod(ToDoListController)
@QtControlFunction()
def recalculate_current_project(self: ToDoListController):
    ''' Recalculate all time stats for current project '''
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
def update_current_project_date(self: ToDoListController):
    ''' Update latest date for project '''
    if project_id := self.model.project_list.current_project_id:
        with execute_layout_change(self.model.project_list):
            update_dict = {
                "last_update": get_date_tuple_now(),
            }
            self.model.project_list.update_project_data(project_id, **update_dict)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def delete_current_project(self: ToDoListController, _click: bool):
    ''' Delete project if selected '''
    if (project_id := self.model.project_list.current_project_id) and \
       (new_project_list := self.model.project_list.delete_selected_project()):

        self.model.project_list = new_project_list
        update_pandas_table_in_layout(self.layout.project_tableView, self.model.project_list)

        self.layout.project_tableView.clearSelection()
        self.layout.newTask_lineEdit.setEnabled(False)
        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.deleteTask_pushButton.setEnabled(False)
        self.layout.taskDescription_textEdit.setText("")
        self.layout.taskDescription_textEdit.setEnabled(False)
        disable_time_edits(self)

        delete_all_items_with_project_id(self.model, project_id)

        self.layout.deleteProject_pushButton.setEnabled(False)
        self.layout.projectDescription_textEdit.setText("")
        self.layout.projectDescription_textEdit.setEnabled(False)

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


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def toggle_record_time(self: ToDoListController, _click: bool):
    ''' Turn time recording time on or off '''
    is_recording = self.timer.toggle_recording()
    if is_recording:
        loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/RecordingButton.qss")
    else:
        loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")
