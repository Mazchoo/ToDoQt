import os
import sys
sys.path.append(os.getcwd())

from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss

from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController

# ToDo Add QML widget which is only visible when saving to Git
# ToDo Only add update files where contents have changed

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loadQss(app, "Resources/QSS/ToDoApp.qss")

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    parent_window.show()

    sys.exit(app.exec_())
