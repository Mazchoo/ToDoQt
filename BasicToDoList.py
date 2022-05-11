import os
import sys
sys.path.append(os.getcwd())

from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.QtHelpers import loadQss

from UI.ToDoLayout import Ui_ToDoLayout
from Models.ToDoModel import ToDoModel
from Controller.ControlFunctions import ToDoListController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loadQss(app, "ToDoApp.qss")

    parent_window = QMainWindow()
    widget = ToDoListController(parent_window, ToDoModel, Ui_ToDoLayout)
    parent_window.show()

    sys.exit(app.exec_())
