
import os
from PyQt5.QtGui import QIcon
from pyqss import Qss as QssEditor

CWD = os.getcwd()
QSS_CACHE = {}


def loadQss(component, file_name):
    path = f"{CWD}/{file_name}"

    if path not in QSS_CACHE:
        with open(path, 'r') as f:
            QSS_CACHE[path] = f.read()

    component.setStyleSheet(QSS_CACHE[path])


def setWindowIcon(widget, file_name):
    icon = QIcon(f"{CWD}/{file_name}")
    widget.setWindowIcon(icon)


def attachQssEditor(window):
    qss_editor = QssEditor(window)
    qss_editor.show()
