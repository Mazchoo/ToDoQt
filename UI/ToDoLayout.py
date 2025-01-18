# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Development\ToDoQt\UI\ToDoApp.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ToDoLayout(object):
    def setupUi(self, ToDoLayout):
        ToDoLayout.setObjectName("ToDoLayout")
        ToDoLayout.setEnabled(True)
        ToDoLayout.resize(1850, 900)
        ToDoLayout.setMinimumSize(QtCore.QSize(1850, 900))
        ToDoLayout.setMaximumSize(QtCore.QSize(1850, 900))
        self.centralwidget = QtWidgets.QWidget(ToDoLayout)
        self.centralwidget.setObjectName("centralwidget")
        self.addNewTask_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addNewTask_pushButton.setEnabled(False)
        self.addNewTask_pushButton.setGeometry(QtCore.QRect(1150, 5, 151, 41))
        self.addNewTask_pushButton.setObjectName("addNewTask_pushButton")
        self.newTask_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.newTask_lineEdit.setGeometry(QtCore.QRect(810, 10, 331, 31))
        self.newTask_lineEdit.setMaxLength(30)
        self.newTask_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.newTask_lineEdit.setObjectName("newTask_lineEdit")
        self.taskDescription_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.taskDescription_textEdit.setEnabled(True)
        self.taskDescription_textEdit.setGeometry(QtCore.QRect(810, 680, 1011, 141))
        self.taskDescription_textEdit.setReadOnly(False)
        self.taskDescription_textEdit.setObjectName("taskDescription_textEdit")
        self.saveTaskChanges_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveTaskChanges_pushButton.setEnabled(False)
        self.saveTaskChanges_pushButton.setGeometry(QtCore.QRect(980, 635, 150, 40))
        self.saveTaskChanges_pushButton.setObjectName("saveTaskChanges_pushButton")
        self.deleteTask_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteTask_pushButton.setEnabled(False)
        self.deleteTask_pushButton.setGeometry(QtCore.QRect(1140, 635, 100, 40))
        self.deleteTask_pushButton.setObjectName("deleteTask_pushButton")
        self.editDescription_label = QtWidgets.QLabel(self.centralwidget)
        self.editDescription_label.setGeometry(QtCore.QRect(820, 646, 151, 20))
        self.editDescription_label.setObjectName("editDescription_label")
        self.backup_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.backup_pushButton.setEnabled(False)
        self.backup_pushButton.setGeometry(QtCore.QRect(1450, 830, 121, 40))
        self.backup_pushButton.setObjectName("backup_pushButton")
        self.close_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.close_pushButton.setGeometry(QtCore.QRect(1710, 830, 121, 40))
        self.close_pushButton.setObjectName("close_pushButton")
        self.upload_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.upload_pushButton.setEnabled(False)
        self.upload_pushButton.setGeometry(QtCore.QRect(1580, 830, 121, 40))
        self.upload_pushButton.setObjectName("upload_pushButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(810, 100, 1011, 521))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.note_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.note_layout.setContentsMargins(0, 0, 0, 0)
        self.note_layout.setObjectName("note_layout")
        self.pending_listView = QtWidgets.QListView(self.horizontalLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.pending_listView.setPalette(palette)
        self.pending_listView.setObjectName("pending_listView")
        self.note_layout.addWidget(self.pending_listView)
        self.inProgress_listView = QtWidgets.QListView(self.horizontalLayoutWidget)
        self.inProgress_listView.setObjectName("inProgress_listView")
        self.note_layout.addWidget(self.inProgress_listView)
        self.done_listView = QtWidgets.QListView(self.horizontalLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.done_listView.setPalette(palette)
        self.done_listView.setObjectName("done_listView")
        self.note_layout.addWidget(self.done_listView)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(810, 60, 1011, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.statusTitle_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.statusTitle_layout.setContentsMargins(0, 0, 0, 0)
        self.statusTitle_layout.setObjectName("statusTitle_layout")
        self.pending_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.pending_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pending_label.setObjectName("pending_label")
        self.statusTitle_layout.addWidget(self.pending_label)
        self.inProgress_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.inProgress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.inProgress_label.setObjectName("inProgress_label")
        self.statusTitle_layout.addWidget(self.inProgress_label)
        self.done_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.done_label.setAlignment(QtCore.Qt.AlignCenter)
        self.done_label.setWordWrap(False)
        self.done_label.setObjectName("done_label")
        self.statusTitle_layout.addWidget(self.done_label)
        self.loaderAnimation_label = QtWidgets.QLabel(self.centralwidget)
        self.loaderAnimation_label.setGeometry(QtCore.QRect(1400, 830, 40, 40))
        self.loaderAnimation_label.setText("")
        self.loaderAnimation_label.setObjectName("loaderAnimation_label")
        self.recordingTime_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordingTime_pushButton.setEnabled(False)
        self.recordingTime_pushButton.setGeometry(QtCore.QRect(1250, 635, 111, 40))
        self.recordingTime_pushButton.setObjectName("recordingTime_pushButton")
        self.projectDescription_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.projectDescription_textEdit.setEnabled(True)
        self.projectDescription_textEdit.setGeometry(QtCore.QRect(30, 680, 721, 141))
        self.projectDescription_textEdit.setReadOnly(False)
        self.projectDescription_textEdit.setObjectName("projectDescription_textEdit")
        self.editProjectDescription_label = QtWidgets.QLabel(self.centralwidget)
        self.editProjectDescription_label.setGeometry(QtCore.QRect(40, 646, 181, 20))
        self.editProjectDescription_label.setObjectName("editProjectDescription_label")
        self.project_label = QtWidgets.QLabel(self.centralwidget)
        self.project_label.setGeometry(QtCore.QRect(30, 60, 721, 39))
        self.project_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project_label.setObjectName("project_label")
        self.timeSpent_timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeSpent_timeEdit.setEnabled(True)
        self.timeSpent_timeEdit.setGeometry(QtCore.QRect(1380, 635, 81, 40))
        self.timeSpent_timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeSpent_timeEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.timeSpent_timeEdit.setObjectName("timeSpent_timeEdit")
        self.estimate_label = QtWidgets.QLabel(self.centralwidget)
        self.estimate_label.setGeometry(QtCore.QRect(1480, 646, 91, 20))
        self.estimate_label.setObjectName("estimate_label")
        self.estimatedTime_timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.estimatedTime_timeEdit.setEnabled(True)
        self.estimatedTime_timeEdit.setGeometry(QtCore.QRect(1580, 635, 81, 40))
        self.estimatedTime_timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.estimatedTime_timeEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.estimatedTime_timeEdit.setObjectName("estimatedTime_timeEdit")
        self.points_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.points_spinBox.setGeometry(QtCore.QRect(1750, 635, 71, 40))
        self.points_spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.points_spinBox.setMaximum(1000)
        self.points_spinBox.setObjectName("points_spinBox")
        self.points_label = QtWidgets.QLabel(self.centralwidget)
        self.points_label.setGeometry(QtCore.QRect(1680, 646, 61, 20))
        self.points_label.setObjectName("points_label")
        self.newProject_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.newProject_lineEdit.setGeometry(QtCore.QRect(50, 10, 331, 31))
        self.newProject_lineEdit.setMaxLength(25)
        self.newProject_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.newProject_lineEdit.setObjectName("newProject_lineEdit")
        self.addNewProject_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addNewProject_pushButton.setEnabled(False)
        self.addNewProject_pushButton.setGeometry(QtCore.QRect(390, 5, 191, 41))
        self.addNewProject_pushButton.setObjectName("addNewProject_pushButton")
        self.project_tableView = QtWidgets.QTableView(self.centralwidget)
        self.project_tableView.setGeometry(QtCore.QRect(30, 106, 721, 514))
        self.project_tableView.setObjectName("project_tableView")
        self.saveProjectChanges_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveProjectChanges_pushButton.setEnabled(False)
        self.saveProjectChanges_pushButton.setGeometry(QtCore.QRect(230, 635, 150, 40))
        self.saveProjectChanges_pushButton.setObjectName("saveProjectChanges_pushButton")
        self.deleteProject_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteProject_pushButton.setEnabled(False)
        self.deleteProject_pushButton.setGeometry(QtCore.QRect(390, 635, 100, 40))
        self.deleteProject_pushButton.setObjectName("deleteProject_pushButton")
        ToDoLayout.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ToDoLayout)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1850, 26))
        self.menubar.setObjectName("menubar")
        ToDoLayout.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ToDoLayout)
        self.statusbar.setObjectName("statusbar")
        ToDoLayout.setStatusBar(self.statusbar)

        self.retranslateUi(ToDoLayout)
        QtCore.QMetaObject.connectSlotsByName(ToDoLayout)

    def retranslateUi(self, ToDoLayout):
        _translate = QtCore.QCoreApplication.translate
        ToDoLayout.setWindowTitle(_translate("ToDoLayout", "MainWindow"))
        self.addNewTask_pushButton.setText(_translate("ToDoLayout", "Add New Task"))
        self.saveTaskChanges_pushButton.setText(_translate("ToDoLayout", "Save Changes"))
        self.deleteTask_pushButton.setText(_translate("ToDoLayout", "Delete"))
        self.editDescription_label.setText(_translate("ToDoLayout", "Task Description"))
        self.backup_pushButton.setText(_translate("ToDoLayout", "Backup"))
        self.close_pushButton.setText(_translate("ToDoLayout", "Close"))
        self.upload_pushButton.setText(_translate("ToDoLayout", "Upload"))
        self.pending_label.setText(_translate("ToDoLayout", "Pending"))
        self.inProgress_label.setText(_translate("ToDoLayout", "In Progress"))
        self.done_label.setText(_translate("ToDoLayout", "Done"))
        self.recordingTime_pushButton.setText(_translate("ToDoLayout", "Log Time"))
        self.editProjectDescription_label.setText(_translate("ToDoLayout", "Project Description"))
        self.project_label.setText(_translate("ToDoLayout", "Project Summaries"))
        self.estimate_label.setText(_translate("ToDoLayout", "Estimate:"))
        self.points_label.setText(_translate("ToDoLayout", "Points:"))
        self.addNewProject_pushButton.setText(_translate("ToDoLayout", "Add New Project"))
        self.saveProjectChanges_pushButton.setText(_translate("ToDoLayout", "Save Changes"))
        self.deleteProject_pushButton.setText(_translate("ToDoLayout", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ToDoLayout = QtWidgets.QMainWindow()
    ui = Ui_ToDoLayout()
    ui.setupUi(ToDoLayout)
    ToDoLayout.show()
    sys.exit(app.exec_())
