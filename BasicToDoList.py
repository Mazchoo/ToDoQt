
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss
from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController

# ToDo - Check what happens when upload is done and there is nothing to push
# ToDo - Enable backup when there are uncommitted changes
# ToDo - Allow editing of title to persist in saved data
# ToDo - Disallow editing of an empty note
# ToDo - Allow the window to be resizeable


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loadQss(app, "Resources/QSS/ToDoApp.qss")

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    parent_window.show()

    sys.exit(app.exec_())
