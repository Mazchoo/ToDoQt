from PyQt5.QtCore import QThread

from git import Repo, Git
from os import getcwd

from Common.GitCommands import (
    git_restore, git_commit, git_push, git_add,
    get_all_changed_files_in_repo_folder,
    get_all_new_files_in_repo_folder
)


CWD = getcwd()
CURRENT_REPO = Repo(CWD)
GIT_EXEC = Git(CWD)


def git_add_all_files_in_folder(folder_path: str):
    changed_files = get_all_changed_files_in_repo_folder(folder_path, CURRENT_REPO)
    changed_files.extend(get_all_new_files_in_repo_folder(folder_path, CURRENT_REPO))

    return [git_add(path, GIT_EXEC) for path in changed_files]


class UploadToGitThread(QThread):
    running = False

    def run(self):
        git_restore('--staged SavedToDo', GIT_EXEC)
        if git_add_all_files_in_folder('SavedToDo'):
            git_commit('Updated ToDo items', GIT_EXEC)
            git_push(GIT_EXEC)


UPLOAD_THREAD_SINGLETON = UploadToGitThread()
