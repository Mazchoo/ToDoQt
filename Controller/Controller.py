''' Main controller module to create to do controller '''
from PyQt5.QtWidgets import QWidget, QListView
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt

from Common.QtHelpers import setWindowIcon
from Common.ModelViewController import CreateQtController
from Controller.ControlHelpers import replace_table_view_in_layout

from Events.DragEvents import enter_task_list_box, drag_move_event, move_task_list_item
from Events.MarkdownEvents import MarkdownFocusHandler
from Events.TimerEvents import TimerEvents


@CreateQtController  # initialise with window, model, layout
class ToDoListController(QWidget):
    ''' Sets up models, callbacks and UI for todo list implementation '''

    def __init__(self, *_args, **_kwargs):
        super().__init__()
        self.loader_animation = QMovie('Resources/Animations/loader.gif')
        self.loader_animation.setScaledSize(QSize().scaled(40, 40, Qt.KeepAspectRatio))

    @staticmethod
    def setupCallbacks(controller):
        ''' Override add callbacks to layout of controller '''
        pending_list = controller.layout.pending_listView
        in_progress_list = controller.layout.inProgress_listView
        done_list = controller.layout.done_listView

        controller.layout.deleteTask_pushButton.clicked.connect(lambda x: controller.delete_current_task(x))
        controller.layout.close_pushButton.clicked.connect(lambda x: controller.close_window(x))

        pending_list.clicked.connect(lambda x: controller.setFocus_to_pendingView(x))
        in_progress_list.clicked.connect(lambda x: controller.setFocus_to_in_progressView(x))
        done_list.clicked.connect(lambda x: controller.setFocus_to_doneView(x))

        controller.layout.backup_pushButton.clicked.connect(lambda x: controller.save_backups(x))
        controller.layout.upload_pushButton.clicked.connect(lambda x: controller.git_push_backups(x))

        setattr(pending_list, 'dragEnterEvent', lambda e: enter_task_list_box(controller.layout, pending_list, e))
        setattr(pending_list, 'dragMoveEvent', lambda e: drag_move_event(pending_list, e))
        setattr(pending_list, 'dropEvent', lambda e: move_task_list_item(controller, pending_list, e))

        setattr(in_progress_list, 'dragEnterEvent', lambda e: enter_task_list_box(controller.layout, in_progress_list, e))
        setattr(in_progress_list, 'dragMoveEvent', lambda e: drag_move_event(in_progress_list, e))
        setattr(in_progress_list, 'dropEvent', lambda e: move_task_list_item(controller, in_progress_list, e))

        setattr(done_list, 'dragEnterEvent', lambda e: enter_task_list_box(controller.layout, done_list, e))
        setattr(done_list, 'dragMoveEvent', lambda e: drag_move_event(done_list, e))
        setattr(done_list, 'dropEvent', lambda e: move_task_list_item(controller, done_list, e))

        controller.layout.addNewTask_pushButton.clicked.connect(lambda x: controller.add_new_task_to_pending(x))
        controller.layout.taskDescription_textEdit.textChanged.connect(lambda: controller.check_enable_task_save_changes())
        controller.layout.newTask_lineEdit.textChanged.connect(lambda: controller.enable_add_new_task())
        controller.layout.saveTaskChanges_pushButton.clicked.connect(lambda x: controller.save_current_task_description(x))

        controller.layout.addNewProject_pushButton.clicked.connect(lambda x: controller.add_new_project(x))
        controller.layout.projectDescription_textEdit.textChanged.connect(lambda: controller.check_enable_project_save())
        controller.layout.newProject_lineEdit.textChanged.connect(lambda: controller.enable_add_new_project())
        controller.layout.saveProjectChanges_pushButton.clicked.connect(lambda x: controller.save_project_description(x))
        controller.layout.deleteProject_pushButton.clicked.connect(lambda x: controller.delete_current_project(x))

        controller.layout.timeSpent_timeEdit.timeChanged.connect(lambda x: controller.edit_time_spent_spinner(x))
        controller.layout.estimatedTime_timeEdit.timeChanged.connect(lambda x: controller.edit_time_estimate_spinner(x))
        controller.layout.points_spinBox.valueChanged.connect(lambda x: controller.edit_points_spinner(x))

        controller.model.pending_list.dataChanged.connect(lambda: controller.task_title_changed())

        controller.task_description_handler = MarkdownFocusHandler(controller.layout.taskDescription_textEdit)
        controller.project_description_handler = MarkdownFocusHandler(controller.layout.projectDescription_textEdit)

        controller.timer = TimerEvents(controller.layout.timeSpent_timeEdit)
        controller.layout.recordingTime_pushButton.clicked.connect(lambda x: controller.toggle_record_time(x))

    @staticmethod
    def initializeModels(controller):
        ''' Override load and set models '''
        controller.model.load_from_folder("SavedToDo")
        controller.layout.pending_listView.setModel(controller.model.pending_filter)
        controller.layout.inProgress_listView.setModel(controller.model.in_progress_filter)
        controller.layout.done_listView.setModel(controller.model.done_filter)

    @staticmethod
    def initializeUi(controller):
        ''' Override to set properties of ui components '''
        controller.parent.setWindowTitle(" To Do List")
        setWindowIcon(controller.parent, 'Resources/Icons/WoodenBow.png')

        controller.layout.pending_listView.setAcceptDrops(True)
        controller.layout.pending_listView.setDragEnabled(True)
        controller.layout.pending_listView.setMovement(QListView.Snap)

        controller.layout.inProgress_listView.setAcceptDrops(True)
        controller.layout.inProgress_listView.setDragEnabled(True)
        controller.layout.pending_listView.setMovement(QListView.Snap)

        controller.layout.done_listView.setAcceptDrops(True)
        controller.layout.done_listView.setDragEnabled(True)
        controller.layout.pending_listView.setMovement(QListView.Snap)

        controller.layout.loaderAnimation_label.setMovie(controller.loader_animation)
        controller.loader_animation.start()
        controller.layout.loaderAnimation_label.setVisible(False)

        # Not an elegant solution, but replaces component with custom sub class
        replace_table_view_in_layout(controller)

        controller.enable_upload_if_uncomitted_changes()
