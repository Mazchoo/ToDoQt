"""Helpers for control functions"""

from typing import Optional, Self, Tuple
from contextlib import contextmanager

from PyQt5.QtWidgets import QListView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex, QTime

from Models.ToDoModel import ToDoModel
from Models.ModelParameters import (
    LIST_VIEW_TO_STATUS_TYPE,
    DEFAULT_HOUR_TO_POINT_CONVERSION,
)
from Models.ProjectTable import ProjectTableModel
from Models.ProjectProxyFilter import ProjectFilterProxyModel

from Common.GitCommands import (
    get_all_uncomitted_files_in_folder,
    get_all_unpushed_commits_in_folder,
)
from Common.ProjectTableLayout import ProjectTableView
from Common.FlexibleMagicMock import FlexibleMagicMock
from Common.QtWindowHelpers import loadQss

from UI import DisplayParameters
from UI.ToDoLayout import Ui_ToDoLayout

from Controller.UploadGitThread import CURRENT_REPO


def update_standard_item_fields(standard_item: QStandardItemModel, **kwargs):
    """Update fields in standard item with kwargs"""
    selected_item_data = standard_item.data()
    selected_item_data.update(kwargs)
    standard_item.setData(selected_item_data)
    return standard_item


def list_view_has_selected_item(list_view: QListView):
    """Return true if list view as item that has been selected"""
    return bool(list_view.selectedIndexes())


def get_selected_model_index(
    selected_row: int, model_filter: ProjectFilterProxyModel
) -> QModelIndex:
    """Get underlying model index from proxy filter"""
    filter_index = model_filter.index(selected_row, 0)
    return model_filter.mapToSource(filter_index)


def get_selected_item_from_list(
    model_list: QStandardItemModel,
    model_filter: ProjectFilterProxyModel,
    list_view: QListView,
) -> Optional[QStandardItem]:
    """Get model item from selected index in filter"""
    selected_indices = list_view.selectedIndexes()
    if selected_indices:
        model_index = get_selected_model_index(selected_indices[0].row(), model_filter)
        return model_list.itemFromIndex(model_index)
    return None


def delete_item_if_selected(
    model_list: QStandardItemModel,
    model_filter: ProjectFilterProxyModel,
    list_view: QListView,
) -> Optional[QStandardItem]:
    """Delete standard item for selected index in filter"""
    selected_indices = list_view.selectedIndexes()
    if selected_indices:
        model_index = get_selected_model_index(
            selected_indices[0].row(), model_filter
        ).row()
        deleted_item = model_list.takeRow(model_index)[0]
        model_filter.invalidateFilter()
        return deleted_item
    return None


def append_item_to_list_view(
    model_list: QStandardItemModel,
    model_filter: ProjectFilterProxyModel,
    list_view: QListView,
    new_item: Optional[QStandardItem],
) -> Optional[QStandardItem]:
    """Add a new item to model"""
    if not new_item:
        return None

    if list_view.objectName() in LIST_VIEW_TO_STATUS_TYPE:
        update_fields = {"status": LIST_VIEW_TO_STATUS_TYPE[list_view.objectName()]}
        new_item = update_standard_item_fields(new_item, **update_fields)

    model_list.appendRow(new_item)
    model_filter.invalidateFilter()
    return new_item


def get_selected_task(model: ToDoModel, layout: Ui_ToDoLayout):
    """Find the current selected task from task lists"""
    if selected_item := get_selected_item_from_list(
        model.pending_list, model.pending_filter, layout.pending_listView
    ):
        return selected_item
    if selected_item := get_selected_item_from_list(
        model.in_progress_list, model.in_progress_filter, layout.inProgress_listView
    ):
        return selected_item
    if selected_item := get_selected_item_from_list(
        model.done_list, model.done_filter, layout.done_listView
    ):
        return selected_item
    return None


def delete_selected_task(model: ToDoModel, layout: Ui_ToDoLayout):
    """Delete a task if it is selected"""
    if deleted_item := delete_item_if_selected(
        model.pending_list, model.pending_filter, layout.pending_listView
    ):
        return deleted_item
    if deleted_item := delete_item_if_selected(
        model.in_progress_list, model.in_progress_filter, layout.inProgress_listView
    ):
        return deleted_item
    if deleted_item := delete_item_if_selected(
        model.done_list, model.done_filter, layout.done_listView
    ):
        return deleted_item
    return None


def delete_tasks_with_project_id(
    model_list: QStandardItemModel,
    model_filter: ProjectFilterProxyModel,
    project_id: int,
):
    """Delete tasks that have project id"""
    for row in range(model_list.rowCount() - 1, -1, -1):
        if (item := model_list.item(row, 0)) and item.data()[
            "project_id"
        ] == project_id:
            model_list.removeRow(row)

    model_filter.invalidateFilter()


def delete_all_tasks_with_project_id(model: ToDoModel, project_id: int):
    """Delete all task from all lists with project id"""
    delete_tasks_with_project_id(model.pending_list, model.pending_filter, project_id)
    delete_tasks_with_project_id(
        model.in_progress_list, model.in_progress_filter, project_id
    )
    delete_tasks_with_project_id(model.done_list, model.done_filter, project_id)


def get_corresponding_model(
    model: ToDoModel, layout: Ui_ToDoLayout, list_view: QListView
) -> Tuple[Optional[QStandardItemModel], Optional[ProjectFilterProxyModel]]:
    """Get model and model filter given list view"""
    if layout.inProgress_listView == list_view:
        return model.in_progress_list, model.in_progress_filter
    if layout.pending_listView == list_view:
        return model.pending_list, model.pending_filter
    if layout.done_listView == list_view:
        return model.done_list, model.done_filter

    return None, None


def clear_not_selected(layout: Ui_ToDoLayout, list_view: QListView):
    """Clear selections for what has not been selected"""
    if list_view != layout.pending_listView:
        layout.pending_listView.clearSelection()
    if list_view != layout.inProgress_listView:
        layout.inProgress_listView.clearSelection()
    if list_view != layout.done_listView:
        layout.done_listView.clearSelection()


def update_project_table(view: ProjectTableView, new_model: ProjectTableModel):
    """Set the project table view with a new model"""
    view.setModel(new_model)
    view.adjust_size(
        new_model.rowCount(),
        DisplayParameters.PROJECT_TABLE_ROW_HEIGHT,
        DisplayParameters.PROJECT_TABLE_COLUMN_SPACING,
    )


def replace_table_view_in_layout(controller: Self):
    """
    Mutates layout of app on the fly, geometry from TableView in UI is inherited new view.
    Take the existing table view component on the UI layout and
    replace it with specialised Pandas Table Layout.
    """
    placeholder = controller.layout.project_tableView
    projects_model = controller.model.project_list

    if isinstance(controller.parent, FlexibleMagicMock):
        projects_view = FlexibleMagicMock()
    else:
        projects_view = ProjectTableView(
            controller.parent, placeholder.geometry().height()
        )

    projects_view.setGeometry(placeholder.geometry())
    controller.parent.layout().replaceWidget(
        controller.layout.project_tableView, projects_view
    )
    update_project_table(projects_view, projects_model)
    placeholder.deleteLater()

    controller.layout.project_tableView = projects_view


def not_uploaded_changes_present() -> bool:
    """Return true if changes still need to be uploaded"""
    return any(
        [
            get_all_uncomitted_files_in_folder("SavedToDo", CURRENT_REPO),
            get_all_unpushed_commits_in_folder("SavedToDo", CURRENT_REPO),
        ]
    )


def filter_available_tasks_for_selected_project(
    model: ToDoModel, project_id: Optional[int]
):
    """Set project id with task views, filter view of tasks by project id"""
    model.pending_filter.set_filter_lambda(project_id)
    model.in_progress_filter.set_filter_lambda(project_id)
    model.done_filter.set_filter_lambda(project_id)


def recalculate_hours_spent(model: ToDoModel, project_id: int) -> float:
    """Return hours spent from all tasks in current project"""
    hr_spent = 0.0
    for i in range(model.pending_list.rowCount()):
        task_data = model.pending_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            hr_spent += task_data["time_spent_seconds"] / 3600

    for i in range(model.in_progress_list.rowCount()):
        task_data = model.in_progress_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            hr_spent += task_data["time_spent_seconds"] / 3600

    for i in range(model.done_list.rowCount()):
        task_data = model.done_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            hr_spent += task_data["time_spent_seconds"] / 3600

    return hr_spent


def recalculate_hours_remain(model: ToDoModel, project_id: int) -> float:
    """Calculate total remaining time from all tasks"""
    hr_remain = 0.0
    for i in range(model.pending_list.rowCount()):
        task_data = model.pending_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            task_remain = task_data["estimated_time_seconds"] / 3600
            task_spent = task_data["time_spent_seconds"] / 3600
            task_diff = task_remain - task_spent
            remain = task_diff if task_diff > 0 else task_spent * 0.25
            hr_remain += remain

    for i in range(model.in_progress_list.rowCount()):
        task_data = model.in_progress_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            task_remain = task_data["estimated_time_seconds"] / 3600
            task_spent = task_data["time_spent_seconds"] / 3600
            task_diff = task_remain - task_spent
            remain = task_diff if task_diff > 0 else task_spent * 0.25
            hr_remain += remain

    return hr_remain


def recalculate_total_points(model: ToDoModel, project_id: int):
    """Recalculate completed points from all tasks"""
    total_points = 0
    for i in range(model.done_list.rowCount()):
        task_data = model.done_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            total_points += task_data["points"]

    return total_points


def get_seconds_from_qt_time(time: QTime) -> int:
    """Convert QTime to total in seconds"""
    return QTime(0, 0, 0).secsTo(time)


def get_qt_time_from_seconds(total_seconds: int) -> QTime:
    """Convert total seconds into a QTime"""
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return QTime(hours, minutes, seconds)


@contextmanager
def block_signals(widget: QWidget):
    """Stop signals from affecting widget in context"""
    was_blocked = widget.blockSignals(True)
    try:
        yield widget
    finally:
        widget.blockSignals(was_blocked)


@contextmanager
def execute_layout_change(widget: QWidget):
    """Context for changing layout with calculation of new state in between"""
    widget.layoutAboutToBeChanged.emit()
    try:
        yield widget
    finally:
        widget.layoutChanged.emit()


def enable_time_edits(self: Self, selected_task: QStandardItem):
    """Set up time edits for selected task"""
    self.layout.timeSpent_timeEdit.setEnabled(True)
    self.layout.estimatedTime_timeEdit.setEnabled(True)
    self.layout.points_spinBox.setEnabled(True)

    self.layout.timerAnimation_label.setVisible(False)
    self.timer.stop_recording()
    loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")

    with block_signals(self.layout.timeSpent_timeEdit) as time_spent_spinner:
        time_spent_spinner.setTime(
            get_qt_time_from_seconds(selected_task.data()["time_spent_seconds"])
        )
    with block_signals(self.layout.estimatedTime_timeEdit) as estimate_spinner:
        estimate_spinner.setTime(
            get_qt_time_from_seconds(selected_task.data()["estimated_time_seconds"])
        )
    with block_signals(self.layout.points_spinBox) as points_spinner:
        points_spinner.setValue(selected_task.data()["points"])


def disable_time_edits(self: Self):
    """Clear time edits"""
    self.layout.timeSpent_timeEdit.setEnabled(False)
    self.layout.estimatedTime_timeEdit.setEnabled(False)
    self.layout.points_spinBox.setEnabled(False)
    self.layout.recordingTime_pushButton.setEnabled(False)

    self.layout.timerAnimation_label.setVisible(False)
    self.timer.stop_recording()
    loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")

    with block_signals(self.layout.timeSpent_timeEdit) as time_spent_spinner:
        time_spent_spinner.setTime(QTime(0, 0, 0))
    with block_signals(self.layout.estimatedTime_timeEdit) as estimate_spinner:
        estimate_spinner.setTime(QTime(0, 0, 0))
    with block_signals(self.layout.points_spinBox) as points_spinner:
        points_spinner.setValue(0)


def get_default_hour_to_points_valuation(
    self: Self, task: QStandardItem, total_seconds: int
) -> int:
    """Set points for estimate if estimate is zero"""
    points = task.data()["points"]
    if points == 0:
        points = (total_seconds // 3600) * DEFAULT_HOUR_TO_POINT_CONVERSION

    with block_signals(self.layout.points_spinBox) as points_spinner:
        points_spinner.setValue(points)

    return points


def clear_all_task_selections(self: Self):
    """Clear task selections on GUI"""
    self.layout.pending_listView.clearSelection()
    self.layout.inProgress_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    self.layout.taskDescription_textEdit.setText("")
    self.layout.deleteTask_pushButton.setEnabled(False)

    disable_time_edits(self)


def clear_new_task_entry(self: Self):
    """Clear the text of new task"""
    self.layout.newTask_lineEdit.setText("")
    self.layout.addNewTask_pushButton.setEnabled(False)


def enable_task_controls(self: Self):
    """Set-up available controls for a selected task"""
    self.layout.taskDescription_textEdit.setEnabled(True)
    self.task_description_handler.render_markdown()
    self.layout.deleteTask_pushButton.setEnabled(True)


def disable_task_controls(self: Self):
    """Set-up available controls for no task selected"""
    self.layout.deleteTask_pushButton.setEnabled(False)
    self.layout.taskDescription_textEdit.setText("")
    self.layout.taskDescription_textEdit.setEnabled(False)


def enable_new_task_control(self: Self):
    """Enable ability to add new task"""
    self.layout.newTask_lineEdit.setEnabled(True)


def disable_new_task_control(self: Self):
    """Disable ability to add new task"""
    self.layout.taskDescription_textEdit.setText("")
    self.layout.taskDescription_textEdit.setEnabled(False)


def enable_project_controls(self: Self):
    """Set-up available controls for a selected project"""
    self.layout.deleteProject_pushButton.setEnabled(True)
    self.layout.projectDescription_textEdit.setEnabled(True)
    text_descrition = self.model.project_list.current_description
    self.layout.projectDescription_textEdit.setText(text_descrition)
    self.project_description_handler.render_markdown()


def disable_project_controls(self: Self):
    """Set-up available controls for no selected project"""
    self.layout.project_tableView.clearSelection()
    self.layout.deleteProject_pushButton.setEnabled(False)
    self.layout.projectDescription_textEdit.setText("")
    self.layout.projectDescription_textEdit.setEnabled(False)


def clear_new_project_entry(self: Self):
    """Clear the text of new project"""
    self.layout.newProject_lineEdit.setText("")
    self.layout.addNewProject_pushButton.setEnabled(False)
