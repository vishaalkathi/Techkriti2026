def compute_coding_score(coding_data: dict) -> float:
    """
    Compute a simple coding platform score out of 10.
    """
    codeforces_rating = coding_data.get("codeforces_rating", 0)

    score = 0.0

    if codeforces_rating >= 1800:
        score += 6
    elif codeforces_rating >= 1400:
        score += 4
    elif codeforces_rating >= 1200:
        score += 3
    elif codeforces_rating > 0:
        score += 2

    if coding_data.get("leetcode_username"):
        score += 2

    if coding_data.get("codeforces_handle"):
        score += 2

    return round(min(score, 10.0), 2)