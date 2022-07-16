import os
import sys
sys.path.append(os.getcwd())

from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss

from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController

# ToDo - grey out add new item when item is empty
# ToDo - clear selected item after item is dragged
# ToDo - If selected item is not edited then remove save button
if __name__ == '__main__':
    app = QApplication(sys.argv)
    loadQss(app, "Resources/QSS/ToDoApp.qss")

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    parent_window.show()

    sys.exit(app.exec_())
