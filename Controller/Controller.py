
from PyQt5.QtWidgets import QWidget

from Common.QtHelpers import setWindowIcon
from Common.ModelViewController import CreateQtController

@CreateQtController # initialise with window, model, layout
class ToDoListController(QWidget):
    '''
        Abstract Class import with ControlFunctions implementations.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__()

    @staticmethod
    def setupCallbacks(self):
        self.layout.delete_pushButton.clicked.connect(lambda x: self.delete_current_item(self, x))
        self.layout.addNewTask_pushButton.clicked.connect(lambda x: self.add_name_to_list(self, x))

        self.layout.pending_listView.clicked.connect(lambda x: self.setFocus_to_pendingView(self, x))
        self.layout.inProgress_listView.clicked.connect(lambda x: self.setFocus_to_in_progressView(self, x))
        self.layout.done_listView.clicked.connect(lambda x: self.setFocus_to_doneView(self, x))

        self.layout.pending_pushButton.clicked.connect(lambda x: self.setCurrentTask_to_pending(self, x))
        self.layout.inProgress_pushButton.clicked.connect(lambda x: self.setCurrentTask_to_inProgress(self, x))
        self.layout.done_pushButton.clicked.connect(lambda x: self.setCurrentTask_to_done(self, x))
        
        self.layout.saveChanges_pushButton.clicked.connect(lambda x: self.save_current_item_description(self, x))
        self.layout.backup_pushButton.clicked.connect(lambda x: self.save_backups(self, x))

    @staticmethod
    def initializeModels(self):
        self.model.load_from_folder("SavedToDo")
        self.layout.pending_listView.setModel(self.model.pending_list)
        self.layout.inProgress_listView.setModel(self.model.in_progress_list)
        self.layout.done_listView.setModel(self.model.done_list)

    @staticmethod
    def initializeUi(self):
        self.parent.setWindowTitle(" To Do List")
        setWindowIcon(self.parent, 'WoodenBow.png')
    