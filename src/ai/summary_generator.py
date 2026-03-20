def generate_profile_summary(data: dict) -> str:
    github_score = data.get("github_score") or 0
    coding_score = data.get("coding_score") or 0

    cf = data.get("codeforces") or {}
    lc = data.get("leetcode") or {}

    summary = []

    # -------------------------------
    # 🔹 OVERALL
    # -------------------------------
    if github_score > 7 and coding_score > 7:
        summary.append("Strong overall developer profile with balanced coding skills and project quality.")
    elif coding_score > github_score:
        summary.append("Strong problem-solving skills, but project/code quality can improve.")
    else:
        summary.append("Good project work, but competitive programming skills can improve.")

    # -------------------------------
    # 🔹 CODEFORCES
    # -------------------------------
    if cf and "error" not in cf:
        rating = cf.get("current_rating") or 0

        if rating > 1800:
            summary.append("Excellent competitive programming performance on Codeforces.")
        elif rating > 1200:
            summary.append("Moderate Codeforces performance with growth potential.")
        else:
            summary.append("Beginner-level Codeforces performance.")

    # -------------------------------
    # 🔹 LEETCODE
    # -------------------------------
    if lc and "error" not in lc:
        hard = lc.get("hard_solved") or 0

        if hard > 30:
            summary.append("Strong exposure to hard DSA problems.")
        elif hard > 0:
            summary.append("Limited hard problem practice on LeetCode.")
        else:
            summary.append("Needs more problem-solving practice on LeetCode.")

    # -------------------------------
    # 🔹 GITHUB QUALITY
    # -------------------------------
    mi = data.get("github_maintainability_index") or 0

    if mi > 70:
        summary.append("Codebase is clean and maintainable.")
    elif mi > 40:
        summary.append("Code quality is moderate but can improve.")
    else:
        summary.append("Code quality and maintainability need improvement.")

    return " ".join(summary)