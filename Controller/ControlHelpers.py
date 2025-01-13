from typing import Optional

from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Models.GlobalParams import LIST_VIEW_TO_STATUS_TYPE
from Models.PandasTable import PandasModel

from Common.GitCommands import (get_all_uncomitted_files_in_folder,
                                get_all_unpushed_commits_in_folder)
from Common.PandasTableLayout import PandasTableView
from Common.FlexibleMagicMock import FlexibleMagicMock

import UI.DisplayParameters as DisplayParameters 
from Controller.UploadGitThread import CURRENT_REPO


def update_standard_item_fields(standard_item: QStandardItemModel, **kwargs):
    selected_item_data = standard_item.data()
    selected_item_data.update(kwargs)
    standard_item.setData(selected_item_data)
    return standard_item


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


def append_item_to_list_view(model_list: QStandardItemModel, list_view: QListView,
                             new_item: Optional[QStandardItem]) -> Optional[QStandardItem]:
    if not new_item:
        return None

    if list_view.objectName() in LIST_VIEW_TO_STATUS_TYPE:
        update_fields = {'status': LIST_VIEW_TO_STATUS_TYPE[list_view.objectName()]}
        new_item = update_standard_item_fields(new_item, **update_fields)

    model_list.appendRow(new_item)
    list_view.setModel(model_list)
    return new_item


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


def get_corresponding_model(model, layout, list_view: QListView):
    corresponding_model = None
    if layout.inProgress_listView == list_view:
        corresponding_model = model.in_progress_list
    elif layout.pending_listView == list_view:
        corresponding_model = model.pending_list
    elif layout.done_listView == list_view:
        corresponding_model = model.done_list

    return corresponding_model


def clear_all_selections(layout):
    layout.pending_listView.clearSelection()
    layout.inProgress_listView.clearSelection()
    layout.done_listView.clearSelection()

    layout.description_textEdit.setText("")
    layout.delete_pushButton.setEnabled(False)
    layout.saveTaskChanges_pushButton.setEnabled(False)


def update_pandas_table_in_layout(view: PandasTableView, new_model: PandasModel):
    view.setModel(new_model)
    view.adjust_size(new_model.rowCount(),
                     DisplayParameters.PROJECT_TABLE_ROW_HEIGHT,
                     DisplayParameters.PROJECT_TABLE_COLUMN_SPACING)


def replace_table_view_in_layout(controller):
    '''
        Take the existing table view component on the UI layout and
        replace it with specialised Pandas Table Layout.
        Mutates layout of app on the fly, geometry from TableView in UI is inherited new view.
    '''
    placeholder = controller.layout.project_tableView
    projects_model = controller.model.project_list

    if isinstance(controller.parent, FlexibleMagicMock):
        projects_view = FlexibleMagicMock()
    else:
        projects_view = PandasTableView(controller.parent, placeholder.geometry().height())

    projects_view.setGeometry(placeholder.geometry())
    controller.parent.layout().replaceWidget(controller.layout.project_tableView, projects_view)
    update_pandas_table_in_layout(projects_view, projects_model)
    placeholder.deleteLater()

    controller.layout.project_tableView = projects_view
    projects_view.clicked.connect(lambda x: controller.project_row_click(controller, x))
    projects_view.horizontalHeader().sectionClicked.connect(
        lambda x: controller.project_header_click(controller, x)
    )


def not_uploaded_changes_present() -> bool:
    return any([get_all_uncomitted_files_in_folder("SavedToDo", CURRENT_REPO),
                get_all_unpushed_commits_in_folder("SavedToDo", CURRENT_REPO)])


def filter_available_tasks_for_selected_project(model, layout):
    pass


def recalculate_stats_for_current_project(model, layout):
    pass


def recalculate_stats_for_all_projects(model, layout):
    pass
