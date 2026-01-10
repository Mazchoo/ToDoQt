"""Control functions for saving and uploading to git"""

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController
from Controller.UploadGitThread import UPLOAD_THREAD_SINGLETON
from Controller.ControlHelpers import not_uploaded_changes_present


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_backups(self: ToDoListController, _click: bool):
    """Save all model data to folder"""
    self.model.save_to_folder("SavedToDo")
    self.layout.backup_pushButton.setEnabled(False)
    self.layout.upload_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
def start_upload(self: ToDoListController):
    """Set-up GUI for starting upload"""
    self.layout.loaderAnimation_label.setVisible(True)
    UPLOAD_THREAD_SINGLETON.running = True
    UPLOAD_THREAD_SINGLETON.started.disconnect()


@ClassMethod(ToDoListController)
def end_upload(self: ToDoListController):
    """Set-up GUI for finishing upload"""
    self.layout.loaderAnimation_label.setVisible(False)
    UPLOAD_THREAD_SINGLETON.running = False
    UPLOAD_THREAD_SINGLETON.finished.disconnect()
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())


@ClassMethod(ToDoListController)
def git_push_backups(self: ToDoListController, _click: bool):
    """Save backups in repo"""
    if not UPLOAD_THREAD_SINGLETON.running:
        self.layout.upload_pushButton.setEnabled(False)
        UPLOAD_THREAD_SINGLETON.finished.connect(self.end_upload)
        UPLOAD_THREAD_SINGLETON.started.connect(self.start_upload)
        UPLOAD_THREAD_SINGLETON.start()


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_upload_if_uncomitted_changes(self: ToDoListController):
    """Enable upload if changes unuploaded changes present"""
    self.layout.upload_pushButton.setEnabled(not_uploaded_changes_present())
