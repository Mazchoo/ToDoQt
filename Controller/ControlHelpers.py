from typing import Optional
from contextlib import contextmanager

from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex, QTime

from Models.GlobalParams import LIST_VIEW_TO_STATUS_TYPE
from Models.ProjectTable import ProjectTableModel
from Models.ProjectProxyFilter import ProjectFilterProxyModel

from Common.GitCommands import (get_all_uncomitted_files_in_folder,
                                get_all_unpushed_commits_in_folder)
from Common.ProjectTableLayout import ProjectTableView
from Common.FlexibleMagicMock import FlexibleMagicMock
from Common.QtHelpers import loadQss

import UI.DisplayParameters as DisplayParameters 
from Controller.UploadGitThread import CURRENT_REPO


def update_standard_item_fields(standard_item: QStandardItemModel, **kwargs):
    selected_item_data = standard_item.data()
    selected_item_data.update(kwargs)
    standard_item.setData(selected_item_data)
    return standard_item


def list_view_has_selected_item(list_view: QListView):
    return True if list_view.selectedIndexes() else False


def get_selected_model_index(selected_row: int, model_filter: ProjectFilterProxyModel) -> QModelIndex:
    filter_index = model_filter.index(selected_row, 0)
    return model_filter.mapToSource(filter_index)


def get_selected_item_from_list(model_list: QStandardItemModel, model_filter: ProjectFilterProxyModel,
                                list_view: QListView):
    selected_indices = list_view.selectedIndexes()
    if selected_indices:
        model_index = get_selected_model_index(selected_indices[0].row(), model_filter)
        return model_list.itemFromIndex(model_index)


def delete_item_if_selected(model_list: QStandardItemModel, model_filter: ProjectFilterProxyModel,
                            list_view: QListView):
    selected_indices = list_view.selectedIndexes()
    if selected_indices:
        model_index = get_selected_model_index(selected_indices[0].row(), model_filter).row()
        deleted_item = model_list.takeRow(model_index)[0]
        model_filter.invalidateFilter()
        return deleted_item


def append_item_to_list_view(model_list: QStandardItemModel, model_filter: ProjectFilterProxyModel,
                             list_view: QListView, new_item: Optional[QStandardItem]) -> Optional[QStandardItem]:
    if not new_item:
        return None

    if list_view.objectName() in LIST_VIEW_TO_STATUS_TYPE:
        update_fields = {'status': LIST_VIEW_TO_STATUS_TYPE[list_view.objectName()]}
        new_item = update_standard_item_fields(new_item, **update_fields)

    model_list.appendRow(new_item)
    model_filter.invalidateFilter()
    return new_item


def get_selected_task(model, layout):
    if selected_item := get_selected_item_from_list(model.pending_list, model.pending_filter, layout.pending_listView):
        return selected_item
    if selected_item := get_selected_item_from_list(model.in_progress_list, model.in_progress_filter, layout.inProgress_listView):
        return selected_item
    if selected_item := get_selected_item_from_list(model.done_list, model.done_filter, layout.done_listView):
        return selected_item
    return None


def delete_selected_task(model, layout):
    if deleted_item := delete_item_if_selected(model.pending_list, model.pending_filter, layout.pending_listView):
        return deleted_item
    elif deleted_item := delete_item_if_selected(model.in_progress_list, model.in_progress_filter, layout.inProgress_listView):
        return deleted_item
    elif deleted_item := delete_item_if_selected(model.done_list, model.done_filter, layout.done_listView):
        return deleted_item
    else:
        return None


def get_corresponding_model(model, layout, list_view: QListView):
    if layout.inProgress_listView == list_view:
        return model.in_progress_list, model.in_progress_filter
    if layout.pending_listView == list_view:
        return model.pending_list, model.pending_filter
    elif layout.done_listView == list_view:
        return model.done_list, model.done_filter

    return None, None


def clear_all_selections(layout):
    layout.pending_listView.clearSelection()
    layout.inProgress_listView.clearSelection()
    layout.done_listView.clearSelection()

    layout.taskDescription_textEdit.setText("")
    layout.deleteTask_pushButton.setEnabled(False)
    layout.saveTaskChanges_pushButton.setEnabled(False)


def clear_not_selected(layout, list_view: QListView):
    if list_view != layout.pending_listView:
        layout.pending_listView.clearSelection()
    if list_view != layout.inProgress_listView:
        layout.inProgress_listView.clearSelection()
    if list_view != layout.done_listView:
        layout.done_listView.clearSelection()


def update_pandas_table_in_layout(view: ProjectTableView, new_model: ProjectTableModel):
    view.setModel(new_model)
    view.adjust_size(new_model.rowCount(),
                     DisplayParameters.PROJECT_TABLE_ROW_HEIGHT,
                     DisplayParameters.PROJECT_TABLE_COLUMN_SPACING)


def replace_table_view_in_layout(controller):
    '''
        Mutates layout of app on the fly, geometry from TableView in UI is inherited new view.
        Take the existing table view component on the UI layout and
        replace it with specialised Pandas Table Layout.
    '''
    placeholder = controller.layout.project_tableView
    projects_model = controller.model.project_list

    if isinstance(controller.parent, FlexibleMagicMock):
        projects_view = FlexibleMagicMock()
    else:
        projects_view = ProjectTableView(controller.parent, placeholder.geometry().height())

    projects_view.setGeometry(placeholder.geometry())
    controller.parent.layout().replaceWidget(controller.layout.project_tableView, projects_view)
    update_pandas_table_in_layout(projects_view, projects_model)
    placeholder.deleteLater()

    controller.layout.project_tableView = projects_view
    projects_view.clicked.connect(lambda x: controller.project_row_click(controller, x))
    projects_view.horizontalHeader().sectionClicked.connect(
        lambda x: controller.project_header_click(controller, x)
    )
    projects_model.dataUpdated.connect(lambda: controller.enable_project_save(controller))


def not_uploaded_changes_present() -> bool:
    return any([get_all_uncomitted_files_in_folder("SavedToDo", CURRENT_REPO),
                get_all_unpushed_commits_in_folder("SavedToDo", CURRENT_REPO)])


def filter_available_tasks_for_selected_project(model, project_id: Optional[int]):
    model.pending_filter.set_filter_lambda(project_id)
    model.in_progress_filter.set_filter_lambda(project_id)
    model.done_filter.set_filter_lambda(project_id)


def recalculate_hours_spent(model, project_id):
    hr_spent = 0.
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


def recalculate_hours_remain(model, project_id):
    hr_remain = 0.
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


def recalculate_total_points(model, project_id):
    total_points = 0
    for i in range(model.done_list.rowCount()):
        task_data = model.done_list.item(i, 0).data()
        if task_data["project_id"] == project_id:
            total_points += task_data["points"]

    return total_points


def get_seconds_from_qt_time(time: QTime) -> int:
    return QTime(0, 0, 0).secsTo(time)


def get_qt_time_from_seconds(total_seconds: int) -> QTime:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return QTime(hours, minutes, seconds)


@contextmanager
def block_signals(obj):
    was_blocked = obj.blockSignals(True)
    try:
        yield obj
    finally:
        obj.blockSignals(was_blocked)


@contextmanager
def execute_layout_change(obj):
    obj.layoutAboutToBeChanged.emit()
    try:
        yield obj
    finally:
        obj.layoutChanged.emit()


def enable_time_edits(self, selected_item):
    self.layout.timeSpent_timeEdit.setEnabled(True)
    self.layout.estimatedTime_timeEdit.setEnabled(True)
    self.layout.points_spinBox.setEnabled(True)
    self.layout.recordingTime_pushButton.setEnabled(True)
    self.timer.stop_recording()
    loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")

    with block_signals(self.layout.timeSpent_timeEdit) as time_spent_spinner:
        time_spent_spinner.setTime(get_qt_time_from_seconds(selected_item.data()['time_spent_seconds']))
    with block_signals(self.layout.estimatedTime_timeEdit) as estimate_spinner:
        estimate_spinner.setTime(get_qt_time_from_seconds(selected_item.data()['estimated_time_seconds']))
    with block_signals(self.layout.points_spinBox) as points_spinner:
        points_spinner.setValue(selected_item.data()['points'])


def disable_time_edits(self):
    self.layout.timeSpent_timeEdit.setEnabled(False)
    self.layout.estimatedTime_timeEdit.setEnabled(False)
    self.layout.points_spinBox.setEnabled(False)
    self.layout.recordingTime_pushButton.setEnabled(False)
    self.timer.stop_recording()
    loadQss(self.layout.recordingTime_pushButton, "Resources/QSS/NormalButton.qss")

    with block_signals(self.layout.timeSpent_timeEdit) as time_spent_spinner:
        time_spent_spinner.setTime(QTime(0, 0, 0))
    with block_signals(self.layout.estimatedTime_timeEdit) as estimate_spinner:
        estimate_spinner.setTime(QTime(0, 0, 0))
    with block_signals(self.layout.points_spinBox) as points_spinner:
        points_spinner.setValue(0)
