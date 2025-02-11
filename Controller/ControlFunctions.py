''' Functions that change state of the GUI '''
from PyQt5.QtCore import QTime

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction
from Common.QtWindowHelpers import loadQss

from Controller.Controller import ToDoListController
from Controller.UploadGitThread import UPLOAD_THREAD_SINGLETON
from Controller.ControlHelpers import (
    get_selected_task, update_standard_item_fields, not_uploaded_changes_present,
    update_project_table, get_seconds_from_qt_time, disable_time_edits,
    recalculate_hours_spent, recalculate_hours_remain, recalculate_total_points,
    execute_layout_change, delete_all_tasks_with_project_id,
    get_default_hour_to_points_valuation
)

from Models.TaskEntry import get_date_tuple_now

import Controller.TaskControl  # noqa pylint: disable=unused-import
import Controller.ViewLists  # noqa pylint: disable=unused-import
import Controller.ProjectControl  # noqa pylint: disable=unused-import


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
def enable_upload_if_uncomitted_changes(self: ToDoListController):
    ''' Enable upload if changes unuploaded changes present '''
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())


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
        update_project_table(self.layout.project_tableView, self.model.project_list)

        self.layout.project_tableView.clearSelection()
        self.layout.newTask_lineEdit.setEnabled(False)
        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.deleteTask_pushButton.setEnabled(False)
        self.layout.taskDescription_textEdit.setText("")
        self.layout.taskDescription_textEdit.setEnabled(False)
        disable_time_edits(self)

        delete_all_tasks_with_project_id(self.model, project_id)

        self.layout.deleteProject_pushButton.setEnabled(False)
        self.layout.projectDescription_textEdit.setText("")
        self.layout.projectDescription_textEdit.setEnabled(False)

        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def toggle_record_time(self: ToDoListController, _click: bool):
    ''' Turn time recording time on or off '''
    if self.timer.is_recording:
        self.layout.timerAnimation_label.setVisible(False)
        loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")
        self.timer.stop_recording()
    else:
        self.layout.timerAnimation_label.setVisible(True)
        loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/RecordingButton.qss")
        self.timer.start_recording()
