import requests

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

PROFILE_QUERY = """
query userProfile($username: String!) {
  matchedUser(username: $username) {
    username
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
  userContestRanking(username: $username) {
    rating
    attendedContestsCount
    globalRanking
    topPercentage
  }
}
"""


def fetch_leetcode_profile_data(username: str) -> dict:
    response = requests.post(
        LEETCODE_GRAPHQL_URL,
        json={
            "query": PROFILE_QUERY,
            "variables": {"username": username},
        },
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()