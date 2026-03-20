
from src.github_analyzer.analyzer import analyze_github_profile
from src.parsing.coding_platform_fetcher import fetch_codeforces_profile, fetch_leetcode_profile

def build_profile_analytics(candidate_profile: dict) -> dict:
    """
    Build GitHub + coding platform analytics from extracted handles.
    """
    github_username = candidate_profile.get("github_username")
    leetcode_username = candidate_profile.get("leetcode_username")
    codeforces_handle = candidate_profile.get("codeforces_handle")

    github_analysis = analyze_github_profile(github_username)

    codeforces_data = fetch_codeforces_profile(codeforces_handle)
    leetcode_data = fetch_leetcode_profile(leetcode_username)

    coding_analysis = {
        "codeforces_handle": codeforces_handle,
        "codeforces_rating": codeforces_data.get("rating", 0) if codeforces_data else 0,
        "codeforces_max_rating": codeforces_data.get("maxRating", 0) if codeforces_data else 0,
        "codeforces_rank": codeforces_data.get("rank") if codeforces_data else None,
        "leetcode_username": leetcode_username,
        "leetcode_profile_url": leetcode_data.get("leetcode_profile_url") if leetcode_data else None,
    }

    return {
        "github_username": github_username,
        **github_analysis,
        **coding_analysis,
    }