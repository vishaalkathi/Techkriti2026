import os
from git import Repo

BASE_DIR = "src/temp_repos"

def clone_repo(repo_url, repo_name):
    path = os.path.join(BASE_DIR, repo_name)

    if os.path.exists(path):
        return path

    try:
        Repo.clone_from(repo_url, path)
        return path
    except:
        return None