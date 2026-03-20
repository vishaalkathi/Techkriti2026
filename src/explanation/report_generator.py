def generate_skill_reasoning(skill, ev):
    if ev["repo_count"] == 0:
        return f"{skill} is mentioned in resume but lacks GitHub evidence."

    reason = f"{skill} is demonstrated through {ev['repo_count']} repositories"

    if ev.get("recent_activity"):
        reason += ", with recent activity"

    if ev.get("project_types"):
        reason += f", including {', '.join(ev['project_types'])} projects"

    if ev.get("complexity"):
        reason += f" showing {ev['complexity'].lower()} complexity work"

    return reason + "."

def generate_report(candidate_name, skill_results, total_score_dict,skill_evidence):

    total_score = total_score_dict["total_score"]
    breakdown = total_score_dict["breakdown"]

    if total_score >= 80:
        fit = "an excellent fit"
        conclusion = "clearly demonstrates strong alignment with the role requirements."
    elif total_score >= 60:
        fit = "a good fit"
        conclusion = "shows good potential to meet the role requirements."
    elif total_score >= 40:
        fit = "a moderate fit"
        conclusion = "has some relevant skills but may require further development."
    else:
        fit = "not recommended"
        conclusion = "currently does not meet the role requirements effectively."

    matched = skill_results['matched'] or []
    missing = skill_results['missing'] or []
    match_percentage = skill_results['match_percentage']

    evidence_lines = []

    for skill in matched:
        ev = skill_evidence.get(skill, {})

        if ev.get("repo_count", 0) > 0:
            parts = [f"{ev['repo_count']} repos"]

            if ev.get("recent_activity"):
                parts.append("recent activity")

            if ev.get("project_types"):
                parts.append(f"{', '.join(ev['project_types'])} projects")

            if ev.get("complexity"):
                parts.append(f"{ev['complexity']} complexity")

            if ev.get("commit_frequency"):
                parts.append(f"{ev['commit_frequency'].lower()} consistency")

            evidence_lines.append(f"{skill} ({', '.join(parts)})")
        else:
            evidence_lines.append(f"{skill} (resume only)")

    evidence_text = ", ".join(evidence_lines)

    report = {
        "candidate_name": candidate_name,
        "skill_matching": {
            "matched_skills": matched,
            "missing_skills": missing,
            "match_percentage": match_percentage
        },
        "score_breakdown": breakdown,
        "total_score": total_score,
        "fit_conclusion": fit
    }

    paragraph = (
        f"{candidate_name} appears to be a {fit} for the role, scoring {total_score} out of 100. "
        f"Key skills matched include {evidence_text if evidence_text else 'none'}, "
        f"while the candidate is missing {', '.join(missing) if missing else 'none'}. "
        f"With a skill match of {match_percentage}%, combined with their activity and experience, "
        f"this profile {conclusion}"
    )

    return report, paragraph