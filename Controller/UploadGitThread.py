from PyQt5.QtCore import QThread

from git import Repo, Git
from os import getcwd

from Common.GitCommands import (
    git_restore_staged, git_commit, git_push, git_add,
    get_all_uncomitted_files_in_folder
)


CWD = getcwd()
CURRENT_REPO = Repo(CWD)
GIT_EXEC = Git(CWD)


def git_add_all_files_in_folder(folder_path: str):
    changed_files = get_all_uncomitted_files_in_folder(folder_path, CURRENT_REPO)
    return [git_add(path, GIT_EXEC) for path in changed_files]


class UploadToGitThread(QThread):
    running = False

    def run(self):
        git_restore_staged('SavedToDo', GIT_EXEC)  # Restores committed but not pushed
        if git_add_all_files_in_folder('SavedToDo'):
            git_commit('Updated ToDo items', GIT_EXEC)

        git_push(GIT_EXEC)


UPLOAD_THREAD_SINGLETON = UploadToGitThread()
