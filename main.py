
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss  #, attachQssEditor
from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController

# ToDo - Allow editing of task title to persist in saved data
# ToDo - Allow field to be loaded if it is unexpectedly not encrypted
# ToDo - Add time recorder for tasks
# ToDo - Try using markdown for showing and allow editing using text
# ToDo - Made it so unicode emojis can be saved and loaded in titles
# ToDo - Disallow editing of an empty note


if __name__ == '__main__':
    app = QApplication(sys.argv)

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    # attachQssEditor(parent_window)
    parent_window.show()

    loadQss(app, "Resources/QSS/ToDoApp.qss")

    sys.exit(app.exec_())
