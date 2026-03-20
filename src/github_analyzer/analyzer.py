from src.github_analyzer.fetcher import get_repos
from src.github_analyzer.cloner import clone_repo
from src.github_analyzer.quality import analyze_repo_code_quality


def analyze_github_profile(username):
    repos = get_repos(username)

    if not isinstance(repos, list):
        return {"error": "Invalid user"}

    results = []
    total_score = 0

    for repo in repos[:5]:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]

        local_path = clone_repo(clone_url, repo_name)

        if not local_path:
            continue

        quality_score = analyze_repo_code_quality(local_path)

        results.append({
            "repo": repo_name,
            "quality_score": quality_score,
            "stars": repo["stargazers_count"]
        })

        total_score += quality_score

    final_score = round(total_score / len(results), 2) if results else 0

    return {
        "username": username,
        "repo_analysis": results,
        "final_score": final_score
    }