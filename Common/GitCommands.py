from git import Repo, Git, GitError
from pathlib import Path


def git_commit(message: str, git: Git):
    cleaned_message = message.replace('"', '').replace("'", "")
    try:
        git.execute(f'git commit -m "{cleaned_message}"')
    except GitError:
        return False
    else:
        return True


def git_push(git: Git):
    try:
        git.execute('git push')
    except GitError:
        return False
    else:
        return True


def git_add(file_path: str, git: Git):
    try:
        git.execute(f'git add {file_path}')
    except GitError:
        return None
    else:
        return file_path


def git_restore(file_path: str, git: Git):
    try:
        git.execute(f'git restore {file_path}')
    except GitError:
        return None
    else:
        return file_path


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
