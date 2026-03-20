from src.scoring.profile_scoring import compute_profile_score

def compute_evidence_weighted_score(skill_results, skill_evidence):
    matched = skill_results["matched"]
    total_required = len(skill_results["matched"]) + len(skill_results["missing"])

    if total_required == 0:
        return 0

    score = 0

    for skill in matched:
        ev = skill_evidence.get(skill, {})

        if ev.get("confidence") == "HIGH":
            score += 1.0
        elif ev.get("confidence") == "MEDIUM":
            score += 0.7
        elif ev.get("confidence") == "LOW":
            score += 0.4
        else:
            score += 0.2  # resume only

    match_ratio = score / total_required
    return match_ratio * 40

def calculate_score(candidate_data, skill_results, skill_evidence):

    # Skill score (max 40)
    skill_score = compute_evidence_weighted_score(skill_results, skill_evidence)

    # Profile score
    profile_scores = compute_profile_score(candidate_data)

    github_score = (profile_scores["github_score"] / 10) * 30
    coding_score = (profile_scores["coding_score"] / 10) * 30

    total_score = skill_score + github_score + coding_score

    return {
        "total_score": round(float(total_score), 2),
        "breakdown": {
            "skill_match": round(float(skill_score), 2),
            "github": round(float(github_score), 2),
            "coding_profiles": round(float(coding_score), 2)
        }
}