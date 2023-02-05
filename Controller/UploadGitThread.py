
from PyQt5.QtCore import QThread

from Common.GitCommands import (
    git_restore, git_add_all_files_in_folder, git_commit, git_push
)


class UploadToGitThread(QThread):
    running = False

    def run(self):
        git_restore('--staged SavedToDo')
        if git_add_all_files_in_folder('SavedToDo'):
            git_commit('Updated ToDo items')
            git_push()


UPLOAD_THREAD_SINGLETON = UploadToGitThread()
