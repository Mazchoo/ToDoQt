"""Control functions for focus on task lists"""

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController
from Controller.ControlHelpers import get_selected_item_from_list
from Controller.TaskControl import select_current_task


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_pendingView(self: ToDoListController, _click: bool):
    """Set-up GUI for pending view"""
    self.layout.inProgress_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_task = get_selected_item_from_list(
        self.model.pending_list, self.model.pending_filter, self.layout.pending_listView
    )
    select_current_task(self, selected_task)
    self.layout.recordingTime_pushButton.setEnabled(False)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_in_progressView(self: ToDoListController, _click: bool):
    """Set-up GUI for in progress view"""
    self.layout.pending_listView.clearSelection()
    self.layout.done_listView.clearSelection()

    selected_task = get_selected_item_from_list(
        self.model.in_progress_list,
        self.model.in_progress_filter,
        self.layout.inProgress_listView,
    )
    select_current_task(self, selected_task)
    self.layout.recordingTime_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def setFocus_to_doneView(self: ToDoListController, _click: bool):
    """Set-up GUI for in done view"""
    self.layout.inProgress_listView.clearSelection()
    self.layout.pending_listView.clearSelection()

    selected_task = get_selected_item_from_list(
        self.model.done_list, self.model.done_filter, self.layout.done_listView
    )
    select_current_task(self, selected_task)
    self.layout.recordingTime_pushButton.setEnabled(False)
