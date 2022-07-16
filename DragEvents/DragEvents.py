
from Controller.ControlHelpers import (
    list_view_has_selected_item, delete_item_if_selected, append_item_to_list_view
)
from PyQt5.QtCore import Qt

def enterTaskListBox(list_view, event):
    is_model_list_item = event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist')
    list_view_has_focus = list_view_has_selected_item(list_view)

    if is_model_list_item and not list_view_has_focus:
        event.accept()
    else:
        event.ignore()


def dragMoveEvent(list_view, event):
    is_model_list_item = event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist')
    list_view_has_focus = list_view_has_selected_item(list_view)

    if is_model_list_item and not list_view_has_focus:
        event.setDropAction(Qt.MoveAction)
        event.accept()
    else:
        event.ignore()


def getCorrespondingModelFromView(layout, model, view_list):
    '''
        ToDo (Move to control helpers)
    '''
    corresponding_model = None
    if layout.inProgress_listView == view_list:
        corresponding_model = model.in_progress_list
    elif layout.pending_listView == view_list:
        corresponding_model = model.pending_list
    elif layout.done_listView == view_list:
        corresponding_model = model.done_list

    return corresponding_model


def clearAllSelections(layout):
    layout.pending_listView.clearSelection()
    layout.inProgress_listView.clearSelection()
    layout.done_listView.clearSelection()


def moveTaskListItem(layout, model, target_view, event):
    '''
        delete_item_if_selected(source_list, list_view)
        append_item_to_list_view(model_list, list_view, standard_item)
    '''

    target_model = getCorrespondingModelFromView(layout, model, target_view)
    if target_model is None:
        event.ignore()
        return

    source_view = event.source()
    source_model = getCorrespondingModelFromView(layout, model, source_view)
    if source_model is None:
        event.ignore()
        return

    move_item = delete_item_if_selected(source_model, source_view)
    if move_item is None:
        event.ignore()
        return
    append_item_to_list_view(target_model, target_view, move_item)

    clearAllSelections(layout)
    layout.backup_pushButton.setEnabled(True)
    event.accept()
