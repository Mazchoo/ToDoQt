"""Functions that programmatically interact with git repo to provide file uploading"""

from pathlib import Path

from git import Repo, Git, GitError


def git_commit(message: str, git: Git):
    """Attempt to execute a git commit"""
    cleaned_message = message.replace('"', "").replace("'", "")
    try:
        git.execute(f'git commit -m "{cleaned_message}"')
    except GitError as e:
        print(f"Commit error {e}")
        return False
    return True


def git_push(git: Git):
    """Attempt to execute a git push"""
    try:
        git.execute("git push")
    except GitError as e:
        print(f"Push error {e}")
        return False
    return True


def git_add(path: str, git: Git):
    """Attempt to add a file to the git repo"""
    try:
        git.execute(f"git add {path}")
    except GitError as e:
        print(f"Git add error {e}")
        return None
    return path


def git_restore_staged(path: str, git: Git):
    """Attempt to reverse a commit in order to start again"""
    try:
        git.execute(f"git restore --staged {path}")
    except GitError:
        return None
    return path


def path_is_relative_to(path: str, base_path: str) -> bool:
    """Returns True is path is subfolder of other path"""
    try:
        Path(path).relative_to(Path(base_path))
    except ValueError:
        return False
    return True


def get_all_changed_files_in_repo_folder(path: str, repo: Repo):
    """For all files contained in path, find all files changed files from repo's perspective"""
    changed_files = repo.index.diff(None)
    return [f.a_path for f in changed_files if path_is_relative_to(f.a_path, path)]


def get_all_new_files_in_repo_folder(path: str, repo: Repo):
    """Find all files contained in path, that are new files from the repo's perspective"""
    return [f for f in repo.untracked_files if path_is_relative_to(f, path)]


def get_all_uncomitted_files_in_folder(path: str, repo: Repo):
    """Get all files to commit to the repo"""
    files = get_all_new_files_in_repo_folder(path, repo)
    files += get_all_changed_files_in_repo_folder(path, repo)
    return files


def get_all_unpushed_commits_in_folder(path: str, repo: Repo):
    """Find any unpushed commits in repo which have files contained in folder"""
    branch = repo.active_branch
    commits = repo.iter_commits(f"{branch}@{{u}}..{branch}")

    unpushed_in_folder = []
    for commit in commits:
        if all(path_is_relative_to(f, path) for f in commit.stats.files):
            unpushed_in_folder.append(commit)

    return unpushed_in_folder
