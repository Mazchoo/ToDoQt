from git import Repo, Git, GitError
from pathlib import Path
from shutil import rmtree


def git_commit(message: str, git: Git):
    cleaned_message = message.replace('"', '').replace("'", "")
    try:
        git.execute(f'git commit -m "{cleaned_message}"')
    except GitError as e:
        print(f'Commit error {e}')
        return False
    else:
        return True


def git_push(git: Git):
    try:
        git.execute('git push')
    except GitError as e:
        print(f'Push error {e}')
        return False
    else:
        return True


def git_add(path: str, git: Git):
    try:
        git.execute(f'git add {path}')
    except GitError as e:
        print(f'Git add error {e}')
        return None
    else:
        return path


def git_restore_staged(path: str, git: Git):
    try:
        git.execute(f'git restore --staged {path}')
    except GitError:
        return None
    else:
        return path


def git_reset_directory(directory: str, git: Git):
    try:
        rmtree(directory)
        git.execute(f'git checkout -- {directory}')
    except GitError:
        return False
    except OSError as e:
        print(f"Path cannot be removed {e}")
        return False
    else:
        return True


def path_is_relative_to(path: str, base_path: str):
    try:
        Path(path).relative_to(Path(base_path))
    except ValueError:
        return False
    else:
        return True


def get_all_changed_files_in_repo_folder(path: str, repo: Repo):
    changed_files = repo.index.diff(None)
    return [
        f.a_path for f in changed_files if path_is_relative_to(f.a_path, path)
    ]


def get_all_new_files_in_repo_folder(path: str, repo: Repo):
    return [
        f for f in repo.untracked_files if path_is_relative_to(f, path)
    ]
