"""
Import all functions that change state of the GUI from events on views
This module should be imported into the controller at some level
"""

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController

import Controller.TaskControl  # noqa pylint: disable=unused-import
import Controller.ViewLists  # noqa pylint: disable=unused-import
import Controller.ProjectControl  # noqa pylint: disable=unused-import
import Controller.Backup  # noqa pylint: disable=unused-import
import Controller.Timing  # noqa pylint: disable=unused-import


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def close_window(self: ToDoListController, _click: bool):
    """Close window action"""
    self.parent.close()
