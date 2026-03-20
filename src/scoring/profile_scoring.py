from src.scoring.github_scoring import compute_github_score
from src.scoring.coding_scoring import compute_coding_score


def compute_profile_score(profile_analytics: dict) -> dict:
    github_score = compute_github_score(profile_analytics)
    coding_score = compute_coding_score(profile_analytics)

    overall_score = round((github_score * 0.6) + (coding_score * 0.4), 2)

    return {
        "github_score": github_score,
        "coding_score": coding_score,
        "overall_profile_score": overall_score
    }