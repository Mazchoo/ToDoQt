
from PyQt5.QtWidgets import QWidget, QListView
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt

from Common.QtHelpers import setWindowIcon
from Common.ModelViewController import CreateQtController
from Controller.ControlHelpers import replace_table_view_in_layout

from DragEvents.DragEvents import enter_task_list_box, drag_move_event, move_task_list_item


@CreateQtController  # initialise with window, model, layout
class ToDoListController(QWidget):
    ''' Abstract Class import with ControlFunctions implementations. '''

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.loader_animation = QMovie('Resources/Animations/loader.gif')
        self.loader_animation.setScaledSize(QSize().scaled(40, 40, Qt.KeepAspectRatio))

    @staticmethod
    def setupCallbacks(self):
        pending_list = self.layout.pending_listView
        in_progress_list = self.layout.inProgress_listView
        done_list = self.layout.done_listView

        self.layout.delete_pushButton.clicked.connect(lambda x: self.delete_current_item(self, x))
        self.layout.addNewTask_pushButton.clicked.connect(lambda x: self.add_new_task_to_pending(self, x))
        self.layout.close_pushButton.clicked.connect(lambda x: self.close_window(self, x))

        pending_list.clicked.connect(lambda x: self.setFocus_to_pendingView(self, x))
        in_progress_list.clicked.connect(lambda x: self.setFocus_to_in_progressView(self, x))
        done_list.clicked.connect(lambda x: self.setFocus_to_doneView(self, x))

        self.layout.saveChanges_pushButton.clicked.connect(
            lambda x: self.save_current_item_description(self, x))
        self.layout.backup_pushButton.clicked.connect(lambda x: self.save_backups(self, x))
        self.layout.upload_pushButton.clicked.connect(lambda x: self.git_push_backups(x))

        setattr(pending_list, 'dragEnterEvent', lambda e: enter_task_list_box(pending_list, e))
        setattr(pending_list, 'dragMoveEvent', lambda e: drag_move_event(pending_list, e))
        setattr(pending_list, 'dropEvent', lambda e: move_task_list_item(self.model, self.layout,
                                                                         pending_list, e))

        setattr(in_progress_list, 'dragEnterEvent', lambda e: enter_task_list_box(in_progress_list, e))
        setattr(in_progress_list, 'dragMoveEvent', lambda e: drag_move_event(in_progress_list, e))
        setattr(in_progress_list, 'dropEvent',
                lambda e: move_task_list_item(self.model, self.layout, in_progress_list, e))

        setattr(done_list, 'dragEnterEvent', lambda e: enter_task_list_box(done_list, e))
        setattr(done_list, 'dragMoveEvent', lambda e: drag_move_event(done_list, e))
        setattr(done_list, 'dropEvent', lambda e: move_task_list_item(self.model, self.layout,
                                                                      done_list, e))

        self.layout.description_textEdit.textChanged.connect(lambda: self.enable_save_changes(self))
        self.layout.newTask_lineEdit.textChanged.connect(lambda: self.enable_add_new_task(self))

        self.layout.newProject_lineEdit.textChanged.connect(lambda: self.enable_add_new_project(self))
        self.layout.addNewProject_pushButton.clicked.connect(lambda x: self.add_new_project(self, x))

    @staticmethod
    def initializeModels(self):
        self.model.load_from_folder("SavedToDo")
        self.layout.pending_listView.setModel(self.model.pending_list)
        self.layout.inProgress_listView.setModel(self.model.in_progress_list)
        self.layout.done_listView.setModel(self.model.done_list)

    @staticmethod
    def initializeUi(self):
        self.parent.setWindowTitle(" To Do List")
        setWindowIcon(self.parent, 'Resources/Icons/WoodenBow.png')

        self.layout.pending_listView.setAcceptDrops(True)
        self.layout.pending_listView.setDragEnabled(True)
        self.layout.pending_listView.setMovement(QListView.Snap)

        self.layout.inProgress_listView.setAcceptDrops(True)
        self.layout.inProgress_listView.setDragEnabled(True)
        self.layout.pending_listView.setMovement(QListView.Snap)

        self.layout.done_listView.setAcceptDrops(True)
        self.layout.done_listView.setDragEnabled(True)
        self.layout.pending_listView.setMovement(QListView.Snap)

        self.layout.loaderAnimation_label.setMovie(self.loader_animation)
        self.loader_animation.start()
        self.layout.loaderAnimation_label.setVisible(False)

        replace_table_view_in_layout(self.layout, self.model, self.parent)

        self.enable_upload_if_uncomitted_changes(self)
