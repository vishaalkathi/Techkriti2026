def analyze_leetcode(profile):
    return {
        "username": profile.username,
        "total_solved": profile.total_solved,
        "easy_solved": profile.easy_solved,
        "medium_solved": profile.medium_solved,
        "hard_solved": profile.hard_solved,
        "acceptance_rate": profile.acceptance_rate,
        "contest_rating": profile.contest_rating,
        "contest_count": profile.contest_count,
    }