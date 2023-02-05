
import os
from PyQt5.QtGui import QIcon
from pyqss import Qss as QssEditor

CWD = os.getcwd()


def loadQss(app, file_name):
    with open(f"{CWD}/{file_name}", 'r') as f:
        qss = f.read()
        app.setStyleSheet(qss)


def setWindowIcon(widget, file_name):
    icon = QIcon(f"{CWD}/{file_name}")
    widget.setWindowIcon(icon)


def attachQssEditor(window):
    qss_editor = QssEditor(window)
    qss_editor.show()
