from src.github_analyzer.fetcher import get_repos
from src.github_analyzer.cloner import clone_repo
from src.github_analyzer.quality import analyze_repo_code_quality


def analyze_github_profile(username):
    repos = get_repos(username)

    if not isinstance(repos, list):
        return {"error": "Invalid user"}

    results = []
    total_quality_score = 0
    total_stars = 0

    for repo in repos[:5]:
        repo_name = repo.get("name")
        clone_url = repo.get("clone_url")
        stars = repo.get("stargazers_count", 0)

        local_path = clone_repo(clone_url, repo_name)

        if not local_path:
            continue

        quality_score = analyze_repo_code_quality(local_path)

        results.append({
            "repo": repo_name,
            "quality_score": quality_score,
            "stars": stars
        })

        total_quality_score += quality_score
        total_stars += stars

    # Avoid division by zero
    repo_count = len(results)
    avg_quality = round(total_quality_score / repo_count, 2) if repo_count > 0 else 0

    # ✅ NEW: profile analytics (for scoring)
    profile_analytics = {
        "avg_quality": avg_quality,
        "total_stars": total_stars,
        "repo_count": repo_count
    }

    return {
        "username": username,
        "repo_analysis": results,
        "profile_analytics": profile_analytics
    }