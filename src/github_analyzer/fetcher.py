from dotenv import load_dotenv
import os
import requests

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"

    headers = {}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.json())
        return []

    return response.json()