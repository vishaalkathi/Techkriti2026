def compute_coding_score(profile_analytics: dict) -> float:
    coding = profile_analytics.get("coding_profiles", {})

    overall = coding.get("summary", {}).get("overall_score", 0)

    # Normalize 0–100 → 0–10
    return round(min(overall / 10, 10.0), 2)