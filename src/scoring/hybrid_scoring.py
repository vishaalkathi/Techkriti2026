from src.scoring.profile_scoring import compute_profile_score

def compute_evidence_weighted_score(skill_results, skill_evidence):
    matched = skill_results["matched"]
    total_required = len(skill_results["matched"]) + len(skill_results["missing"])

    if total_required == 0:
        return 0

    
    score=0

    for skill in matched:
        ev = skill_evidence.get(skill, {})
        base = 0
        # Confidence
        if ev.get("confidence") == "HIGH":
            base += 0.5
        elif ev.get("confidence") == "MEDIUM":
            base += 0.3
        elif ev.get("confidence") == "LOW":
            base += 0.2
        else:
            base += 0.1

        # Complexity
        if ev.get("complexity") == "HIGH":
            base += 0.3
        elif ev.get("complexity") == "MEDIUM":
            base += 0.2

        # Commit frequency
        if ev.get("commit_frequency") == "HIGH":
            base += 0.2
        elif ev.get("commit_frequency") == "MEDIUM":
            base += 0.1

        # Impact (stars)
        if ev.get("impact_score", 0) > 50:
            base += 0.2
        elif ev.get("impact_score", 0) > 10:
            base += 0.1

        score += base

    match_ratio = min(score / total_required, 1)
    return match_ratio * 40

def calculate_score(candidate_data, skill_results, skill_evidence, resume_data, jd_data):

    candidate_exp = resume_data.get("experience_years", 0)
    required_exp = jd_data.get("experience_required", 0)

    # Skill score (max 40)
    
    skill_score = compute_evidence_weighted_score(skill_results, skill_evidence)

    missing_count = len(skill_results["missing"])
    penalty = missing_count * 1.5
    skill_score = max(skill_score - penalty, 0)
    
    # Profile score
    profile_scores = compute_profile_score(candidate_data)

    github_score = (profile_scores["github_score"] / 10) * 30
    coding_score = (profile_scores["coding_score"] / 10) * 30

    total_score = skill_score + github_score + coding_score

    experience_score = 0

    candidate_exp = candidate_data.get("experience_years", 0)
    required_exp = candidate_data.get("experience_required", 0)

    if required_exp == 0:
        experience_score = 5
    elif candidate_exp >= required_exp:
        experience_score = 10
    elif candidate_exp >= required_exp * 0.7:
        experience_score = 7
    elif candidate_exp >= required_exp * 0.4:
        experience_score = 4
    elif candidate_exp > 0:
        experience_score = 2

    total_score += experience_score

    return {
        "total_score": round(float(total_score), 2),
        "breakdown": {
            "skill_match": round(float(skill_score), 2),
            "github": round(float(github_score), 2),
            "coding_profiles": round(float(coding_score), 2),
            "experience": round(float(experience_score), 2)
        }
}