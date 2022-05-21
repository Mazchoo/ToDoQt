from git import Repo, Git
from os import getcwd
from pathlib import Path
REPO_DIR = getcwd()

# cwd required for this package is repo directory
CURRENT_REPO = Repo(REPO_DIR)
GIT_EXEC = Git(REPO_DIR)


def git_commit(message: str):
    cleaned_message = message.replace('"', '').replace("'", "")
    GIT_EXEC.execute(f'git commit -m "{cleaned_message}"')


def git_push():
    GIT_EXEC.execute('git push')


def git_add(file_path: str):
    GIT_EXEC.execute(f'git add {file_path}')


def git_restore(file_path: str):
    GIT_EXEC.execute(f'git restore {file_path}')


def path_is_relative_to(path: str, base_path: str):
    try:
        Path(path).relative_to(Path(base_path))
    except:
        return False
    else:
        return True


def git_add_all_files_in_folder(folder_path: str):
    repo_changed_files = CURRENT_REPO.index.diff(None)
    changed_files_in_folder = [
        file.a_path for file in repo_changed_files if path_is_relative_to(file.a_path, folder_path)
    ]
    new_files_in_folder =[
        file for file in CURRENT_REPO.untracked_files if path_is_relative_to(file, folder_path)
    ]
    changed_files_in_folder.extend(new_files_in_folder)
    
    for file_path in changed_files_in_folder:
        git_add(file_path)
    return changed_files_in_folder


if __name__ == '__main__':
    git_restore('--staged SavedToDo')
    if git_add_all_files_in_folder('SavedToDo'):
        git_commit('Updated ToDo items')
        git_push()
