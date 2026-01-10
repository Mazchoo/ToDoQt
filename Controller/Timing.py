"""Control functions that affect points, estimates and timers"""

from PyQt5.QtCore import QTime

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction
from Common.QtWindowHelpers import loadQss

from Controller.Controller import ToDoListController
from Controller.ControlHelpers import (
    get_selected_task,
    update_standard_item_fields,
    get_seconds_from_qt_time,
    recalculate_hours_spent,
    recalculate_hours_remain,
    recalculate_total_points,
    execute_layout_change,
    get_default_hour_to_points_valuation,
)

from Models.TaskEntry import get_date_tuple_now


@ClassMethod(ToDoListController)
@QtControlFunction(QTime(0, 0, 0))
def edit_time_spent_spinner(self: ToDoListController, time: QTime):
    """Recalculate project stats on time spent edit"""
    if selected_task := get_selected_task(self.model, self.layout):
        total_seconds = get_seconds_from_qt_time(time)
        update_standard_item_fields(selected_task, time_spent_seconds=total_seconds)
        self.layout.backup_pushButton.setEnabled(True)
        update_current_project_date(self)
        self.recalculate_current_project()


@ClassMethod(ToDoListController)
@QtControlFunction(QTime(0, 0, 0))
def edit_time_estimate_spinner(self: ToDoListController, time: QTime):
    """Recalculate project stats on time estimate edit"""
    if selected_task := get_selected_task(self.model, self.layout):
        total_seconds = get_seconds_from_qt_time(time)
        points = get_default_hour_to_points_valuation(
            self, selected_task, total_seconds
        )

        update_standard_item_fields(
            selected_task, estimated_time_seconds=total_seconds, points=points
        )
        self.layout.backup_pushButton.setEnabled(True)
        self.recalculate_current_project()


@ClassMethod(ToDoListController)
@QtControlFunction(0.0)
def edit_points_spinner(self: ToDoListController, value: int):
    """Recalculate project stats on points edit"""
    if selected_task := get_selected_task(self.model, self.layout):
        update_standard_item_fields(selected_task, points=value)
        self.layout.backup_pushButton.setEnabled(True)
        self.recalculate_current_project()


@ClassMethod(ToDoListController)
@QtControlFunction()
def recalculate_current_project(self: ToDoListController):
    """Recalculate all time stats for current project"""
    if project_id := self.model.project_list.current_project_id:
        with execute_layout_change(self.model.project_list):
            update_dict = {
                "hr_spent": round(recalculate_hours_spent(self.model, project_id), 1),
                "hr_remain": round(recalculate_hours_remain(self.model, project_id), 1),
                "points_gained": recalculate_total_points(self.model, project_id),
            }
            self.model.project_list.update_project_data(project_id, **update_dict)


@ClassMethod(ToDoListController)
@QtControlFunction()
def update_current_project_date(self: ToDoListController):
    """Update latest date for project"""
    if project_id := self.model.project_list.current_project_id:
        with execute_layout_change(self.model.project_list):
            update_dict = {
                "last_update": get_date_tuple_now(),
            }
            self.model.project_list.update_project_data(project_id, **update_dict)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def toggle_record_time(self: ToDoListController, _click: bool):
    """Turn time recording time on or off"""
    if self.timer.is_recording:
        self.layout.timerAnimation_label.setVisible(False)
        loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")
        self.timer.stop_recording()
    else:
        self.layout.timerAnimation_label.setVisible(True)
        loadQss(
            self.layout.recordingTime_pushButton, "Resources/QSS/RecordingButton.qss"
        )
        self.timer.start_recording()
