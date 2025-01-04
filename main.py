
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss  #, attachQssEditor
from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController

# ToDo - Add the ability to save and load projects
# ToDo - Allow editing of time and points on notes
# ToDo - Add time recorder for notes
# ToDo - Add linking of task to selected project
# ToDo - Calculate totals for each project
# ToDo - Add ability to delete projects
# ToDo - Try using markdown for showing and allow editing using text
# ToDo - Made it so unicode emojis can be saved and loaded in titles
# ToDo - Allow editing of title to persist in saved data
# ToDo - Disallow editing of an empty note


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loadQss(app, "Resources/QSS/ToDoApp.qss")

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    # attachQssEditor(parent_window)
    parent_window.show()

    sys.exit(app.exec_())
