
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent

from Controller.ControlHelpers import (
    list_view_has_selected_item, delete_item_if_selected, append_item_to_list_view,
    get_corresponding_model, clear_all_selections, clear_not_selected
)


def enter_task_list_box(layout, list_view: QListView, event: QDragEnterEvent):
    is_model_list_item = event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist')
    if list_view_has_focus := list_view_has_selected_item(list_view):
        clear_not_selected(layout, list_view)

    if is_model_list_item and not list_view_has_focus:
        event.accept()
    else:
        event.ignore()


def drag_move_event(list_view: QListView, event: QDragMoveEvent):
    is_model_list_item = event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist')
    list_view_has_focus = list_view_has_selected_item(list_view)

    if is_model_list_item and not list_view_has_focus:
        event.setDropAction(Qt.MoveAction)
        event.accept()
    else:
        event.ignore()


def move_task_list_item(model, layout, target_view: QListView, event: QDropEvent):

    target_model, target_filter = get_corresponding_model(model, layout, target_view)
    if target_model is None:
        event.ignore()
        return

    source_view = event.source()
    source_model, source_filter = get_corresponding_model(model, layout, source_view)
    if source_model is None:
        event.ignore()
        return

    move_item = delete_item_if_selected(source_model, source_filter, source_view)
    if move_item is None:
        event.ignore()
        return
    append_item_to_list_view(target_model, target_filter, target_view, move_item)

    clear_all_selections(layout)
    layout.backup_pushButton.setEnabled(True)
    event.accept()
