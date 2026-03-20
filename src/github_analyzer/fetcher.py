from dotenv import load_dotenv
import os
import requests

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

def _get_headers():
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers


def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"

    response = requests.get(url, headers=_get_headers())

    if response.status_code != 200:
        print("Error fetching repos:", response.json())
        return []

    repos = response.json()

    # 🔥 BETTER: sort by importance
    repos = sorted(
        repos,
        key=lambda r: r.get("stargazers_count", 0),
        reverse=True
    )

    return repos


def get_user_profile(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, headers=_get_headers())

    if response.status_code != 200:
        print("Error fetching user:", response.json())
        return {}

    return response.json()


def extract_languages(repos):
    lang_set = set()
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_set.add(lang)
    return list(lang_set)