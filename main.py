
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss  #, attachQssEditor
from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController

# ToDo - Update GUI logic for when a project changes text, content etc
# ToDo - Allow field to be loaded if it is unexpectedly not encrypted
# ToDo - Allow editing of time and points on tasks
# ToDo - Add time recorder for tasks
# ToDo - Add linking of task to selected project
# ToDo - Calculate totals for each project
# ToDo - Add ability to delete projects
# ToDo - Try using markdown for showing and allow editing using text
# ToDo - Made it so unicode emojis can be saved and loaded in titles
# ToDo - Allow editing of title to persist in saved data
# ToDo - Disallow editing of an empty note


if __name__ == '__main__':
    app = QApplication(sys.argv)

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    # attachQssEditor(parent_window)
    parent_window.show()

    loadQss(app, "Resources/QSS/ToDoApp.qss")

    sys.exit(app.exec_())
