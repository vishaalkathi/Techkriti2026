def compute_github_score(github_data: dict) -> float:
    repos = github_data.get("github_public_repos", 0)
    stars = github_data.get("github_total_stars", 0)
    forks = github_data.get("github_total_forks", 0)
    followers = github_data.get("github_followers", 0)
    languages = len(github_data.get("github_top_languages", []))

    # 🔥 NEW METRICS
    avg_complexity = github_data.get("github_avg_complexity", 0)
    mi_score = github_data.get("github_maintainability_index", 0)
    flake8_issues = github_data.get("github_flake8_issues", 0)

    # --- Normalization logic ---
    
    complexity_score = max(0, (10 - avg_complexity)) / 10   # lower is better
    mi_normalized = mi_score / 100                         # already 0–100
    flake8_score = max(0, (50 - flake8_issues)) / 50       # fewer issues better

    score = (
        min(repos / 10, 2.0) +
        min(stars / 20, 1.5) +
        min(forks / 10, 1.0) +
        min(followers / 20, 1.0) +
        min(languages / 5, 1.5) +

        # 🔥 NEW CODE QUALITY BLOCK (TOTAL = 3.0)
        (mi_normalized * 1.5) +
        (complexity_score * 1.0) +
        (flake8_score * 0.5)
    )

    return round(min(score, 10.0), 2)