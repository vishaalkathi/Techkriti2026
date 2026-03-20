from datetime import datetime
from collections import defaultdict

def is_recent(date_str):
    if not date_str:
        return False
    try:
        last_update = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return (datetime.now() - last_update).days < 180
    except:
        return False


def detect_project_type(repo):
    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()

    text = name + " " + desc

    if "ml" in text or "model" in text:
        return "ML"
    if "api" in text or "backend" in text:
        return "Backend"
    if "web" in text or "frontend" in text:
        return "Web"
    return "General"

def compute_repo_complexity(repo):
    score = 0

    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()
    stars = repo.get("stargazers_count", 0) or 0

    text = name + " " + desc

    # 🔹 Keyword-based complexity
    complex_keywords = ["ml", "model", "system", "engine", "api", "backend", "ai"]

    for word in complex_keywords:
        if word in text:
            score += 2

    # 🔹 Stars (real-world usage signal)
    if stars > 50:
        score += 3
    elif stars > 10:
        score += 2
    elif stars > 0:
        score += 1

    # 🔹 Basic classification
    if score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    return "BASIC"

def overall_complexity(levels):
    if "HIGH" in levels:
        return "HIGH"
    if "MEDIUM" in levels:
        return "MEDIUM"
    if "LOW" in levels:
        return "LOW"
    return "BASIC"

def compute_commit_frequency(repos):
    """
    Estimate commit consistency using repo update timestamps.
    """

    monthly_activity = defaultdict(int)

    for repo in repos:
        updated_at = repo.get("updated_at")

        if not updated_at:
            continue

        try:
            dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
            key = f"{dt.year}-{dt.month}"
            monthly_activity[key] += 1
        except:
            continue

    active_months = len(monthly_activity)

    # 🔥 Frequency classification
    if active_months >= 6:
        return "HIGH"
    elif active_months >= 3:
        return "MEDIUM"
    elif active_months >= 1:
        return "LOW"
    return "NONE"


def build_skill_evidence(resume_skills, github_data):

    evidence_map = {}

    repos = github_data.get("repo_metrics", {}).get("repos", [])

    for skill in resume_skills:
        skill_lower = skill.lower()

        repo_count = 0
        recent_flag = False
        project_types = set()
        project_names = []
        complexity_levels = []
        skill_repos = []
        total_stars=0
        for repo in repos:
            repo_lang = (repo.get("language") or "").lower()

            if skill_lower in repo_lang:
                repo_count += 1
                project_names.append(repo.get("name", ""))

                skill_repos.append(repo)

                # recent activity
                if is_recent(repo.get("updated_at")):
                    recent_flag = True

                stars = repo.get("stargazers_count", 0)
                total_stars += stars

                # project type detection
                project_types.add(detect_project_type(repo))

                complexity = compute_repo_complexity(repo)
                complexity_levels.append(complexity)

        # 🔥 Confidence logic (UPGRADED)
        if repo_count >= 5 and recent_flag:
            confidence = "HIGH"
        elif repo_count >= 2:
            confidence = "MEDIUM"
        elif repo_count >= 1:
            confidence = "LOW"
        else:
            confidence = "NONE"

        commit_frequency = compute_commit_frequency(skill_repos)

        evidence_map[skill] = {
            "repo_count": repo_count,
            "recent_activity": recent_flag,
            "project_types": list(project_types),
            "projects": project_names[:3],
            "complexity": overall_complexity(complexity_levels),
            "commit_frequency": commit_frequency,
            "impact_score": total_stars,
            "confidence": confidence
        }

    return evidence_map