def compute_coding_score(data: dict) -> float:
    """
    Computes coding score out of 10 using:
    - Codeforces performance
    - LeetCode performance

    Safe against None / missing values.
    Slightly improved normalization.
    """

    score = 0.0

    codeforces = data.get("codeforces") or {}
    leetcode = data.get("leetcode") or {}

    # -------------------------------
    # 🔹 CODEFORCES SCORING
    # -------------------------------
    if codeforces and "error" not in codeforces:
        rating = codeforces.get("current_rating") or 0
        solved = codeforces.get("total_solved") or 0
        avg_rating = codeforces.get("avg_solved_rating") or 0
        contests = codeforces.get("contest_count") or 0

        # Rating (main signal)
        score += min(rating / 1200, 3.0)          # smoother scaling

        # Problem volume
        score += min(solved / 1000, 2.0)

        # Difficulty level
        score += min(avg_rating / 1500, 2.0)

        # Contest participation
        score += min(contests / 100, 1.5)

    # -------------------------------
    # 🔹 LEETCODE SCORING
    # -------------------------------
    if leetcode and "error" not in leetcode:
        total = leetcode.get("total_solved") or 0
        medium = leetcode.get("medium_solved") or 0
        hard = leetcode.get("hard_solved") or 0
        contest_rating = leetcode.get("contest_rating") or 0

        # Total solved
        score += min(total / 300, 1.5)

        # Medium problems
        score += min(medium / 150, 1.0)

        # Hard problems (important signal)
        score += min(hard / 75, 1.5)

        # Contest rating
        score += min(contest_rating / 2500, 1.5)

    # -------------------------------
    # 🔹 FINAL SCORE
    # -------------------------------
    return round(min(score, 10.0), 2)