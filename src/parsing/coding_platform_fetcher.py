import requests


def fetch_codeforces_profile(codeforces_handle: str) -> dict:
    """
    Fetch Codeforces user info.
    """
    if not codeforces_handle:
        return {}

    url = f"https://codeforces.com/api/user.info?handles={codeforces_handle}"
    response = requests.get(url, timeout=15)

    if response.status_code != 200:
        return {"error": f"Failed to fetch Codeforces data for {codeforces_handle}"}

    data = response.json()

    if data.get("status") != "OK":
        return {"error": f"Invalid Codeforces handle: {codeforces_handle}"}

    return data["result"][0]


def fetch_leetcode_profile(leetcode_username: str) -> dict:
    """
    Placeholder LeetCode fetcher.
    LeetCode does not provide an easy open public REST API like GitHub/Codeforces.
    Start with basic profile link output; later improve with GraphQL or scraping.
    """
    if not leetcode_username:
        return {}

    return {
        "leetcode_username": leetcode_username,
        "leetcode_profile_url": f"https://leetcode.com/u/{leetcode_username}/"
    }