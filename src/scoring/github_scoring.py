def compute_github_score(github_data: dict) -> float:
    repos = github_data.get("github_public_repos", 0)
    stars = github_data.get("github_total_stars", 0)
    forks = github_data.get("github_total_forks", 0)
    followers = github_data.get("github_followers", 0)
    languages = len(github_data.get("github_top_languages", []))
    code_quality = github_data.get("github_avg_code_quality", 0)

    score = (
        min(repos / 10, 2.0) +
        min(stars / 20, 1.5) +
        min(forks / 10, 1.0) +
        min(followers / 20, 1.0) +
        min(languages / 5, 1.5) +
        (code_quality / 100) * 3.0   # 🔥 NEW (MOST IMPORTANT)
    )

    return round(min(score, 10.0), 2)