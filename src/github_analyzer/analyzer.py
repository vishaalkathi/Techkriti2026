from src.github_analyzer.fetcher import get_repos, get_user_profile, extract_languages
from src.github_analyzer.cloner import clone_repo
from src.github_analyzer.quality import analyze_repo_code_quality


def analyze_github_profile(username):
    repos = get_repos(username)
    user_data = get_user_profile(username)
    languages = extract_languages(repos)

    if not isinstance(repos, list):
        return {"error": "Invalid user"}

    results = []

    total_complexity = 0
    total_mi = 0
    total_flake8 = 0
    total_stars = 0

    for repo in repos[:3]:
        repo_name = repo.get("name")
        clone_url = repo.get("clone_url")
        stars = repo.get("stargazers_count", 0)

        print(f"\n🔽 Processing repo: {repo_name}")

        # 🔥 Skip huge repos
        if repo.get("size", 0) > 20000:
            print("⏩ Skipping large repo")
            continue

        local_path = clone_repo(clone_url, repo_name)

        if not local_path:
            print("❌ Clone failed")
            continue

        # 🔥 Analyze repo
        quality = analyze_repo_code_quality(local_path)

        avg_complexity = quality.get("avg_complexity", 0)
        mi_score = quality.get("maintainability_index", 0)
        flake8_issues = quality.get("flake8_issues", 0)

        results.append({
            "repo": repo_name,
            "avg_complexity": avg_complexity,
            "maintainability_index": mi_score,
            "flake8_issues": flake8_issues,
            "stars": stars
        })

        # ✅ INSIDE LOOP
        total_complexity += avg_complexity
        total_mi += mi_score
        total_flake8 += flake8_issues
        total_stars += stars

    repo_count = len(results)

    avg_complexity = round(total_complexity / repo_count, 2) if repo_count else 0
    avg_mi = round(total_mi / repo_count, 2) if repo_count else 0
    avg_flake8 = round(total_flake8 / repo_count, 2) if repo_count else 0

    profile_analytics = {
        "github_public_repos": user_data.get("public_repos", 0),
        "github_total_stars": total_stars,
        "github_total_forks": sum(r.get("forks_count", 0) for r in repos[:3]),
        "github_followers": user_data.get("followers", 0),
        "github_top_languages": languages,

        "github_avg_complexity": avg_complexity,
        "github_maintainability_index": avg_mi,
        "github_flake8_issues": avg_flake8
    }

    return {
        "username": username,
        "repo_analysis": results,
        "profile_analytics": profile_analytics
    }