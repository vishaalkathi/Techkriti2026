
from src.github_analyzer.analyzer import analyze_github_profile
from src.services.coding_profile_service import analyze_coding_profiles

def build_profile_analytics(candidate_profile: dict) -> dict:
    """
    Build GitHub + coding platform analytics from extracted handles.
    """
    github_username = candidate_profile.get("github_username")
    leetcode_username = candidate_profile.get("leetcode_username")
    codeforces_handle = candidate_profile.get("codeforces_handle")

    github_analysis = analyze_github_profile(github_username)

    coding_analysis = analyze_coding_profiles(
        codeforces_handle=codeforces_handle,
        leetcode_username=leetcode_username
    )

    

    return {
        "github_username": github_username,
        **github_analysis,
        "coding_profiles": coding_analysis
    }