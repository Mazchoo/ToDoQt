
from PyQt5.QtWidgets import QWidget, QListView

from Common.QtHelpers import setWindowIcon
from Common.ModelViewController import CreateQtController
from DragEvents.DragEvents import enterTaskListBox, dragMoveEvent, moveTaskListItem


@CreateQtController # initialise with window, model, layout
class ToDoListController(QWidget):
    '''
        Abstract Class import with ControlFunctions implementations.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__()

    @staticmethod
    def setupCallbacks(self):
        pending_list = self.layout.pending_listView
        in_progress_list = self.layout.inProgress_listView
        done_list = self.layout.done_listView

        self.layout.delete_pushButton.clicked.connect(lambda x: self.delete_current_item(self, x))
        self.layout.addNewTask_pushButton.clicked.connect(lambda x: self.add_name_to_list(self, x))
        self.layout.close_pushButton.clicked.connect(lambda x: self.close_window(self, x))

        pending_list.clicked.connect(lambda x: self.setFocus_to_pendingView(self, x))
        in_progress_list.clicked.connect(lambda x: self.setFocus_to_in_progressView(self, x))
        done_list.clicked.connect(lambda x: self.setFocus_to_doneView(self, x))

        self.layout.saveChanges_pushButton.clicked.connect(lambda x: self.save_current_item_description(self, x))
        self.layout.backup_pushButton.clicked.connect(lambda x: self.save_backups(self, x))
        self.layout.upload_pushButton.clicked.connect(lambda x: self.git_push_backups(x))

        setattr(pending_list, 'dragEnterEvent', lambda e: enterTaskListBox(pending_list, e))
        setattr(pending_list, 'dragMoveEvent', lambda e: dragMoveEvent(pending_list, e))
        setattr(pending_list, 'dropEvent', lambda e: moveTaskListItem(self.layout, self.model, pending_list, e))

        setattr(in_progress_list, 'dragEnterEvent', lambda e: enterTaskListBox(in_progress_list, e))
        setattr(in_progress_list, 'dragMoveEvent', lambda e: dragMoveEvent(in_progress_list, e))
        setattr(in_progress_list, 'dropEvent', lambda e: moveTaskListItem(self.layout, self.model, in_progress_list, e))

        setattr(done_list, 'dragEnterEvent', lambda e: enterTaskListBox(done_list, e))
        setattr(done_list, 'dragMoveEvent', lambda e: dragMoveEvent(done_list, e))
        setattr(done_list, 'dropEvent', lambda e: moveTaskListItem(self.layout, self.model, done_list, e))

        self.layout.description_textEdit.textChanged.connect(lambda: self.enable_save_changes(self))
        self.layout.newTask_lineEdit.textChanged.connect(lambda: self.enable_add_new_item(self))

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
