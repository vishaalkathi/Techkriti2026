import requests


BASE = "https://codeforces.com/api"


def fetch_user_info(handle: str) -> dict:
    url = f"{BASE}/user.info?handles={handle}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_user_rating(handle: str) -> dict:
    url = f"{BASE}/user.rating?handle={handle}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_user_status(handle: str) -> dict:
    url = f"{BASE}/user.status?handle={handle}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()