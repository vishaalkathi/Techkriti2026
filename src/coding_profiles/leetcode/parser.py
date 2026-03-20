from src.coding_profiles.models import LeetCodeProfile


def parse_leetcode_profile(username: str, data: dict) -> LeetCodeProfile:
    matched_user = data["data"].get("matchedUser")
    contest_data = data["data"].get("userContestRanking")

    if not matched_user:
        raise ValueError(f"LeetCode user '{username}' not found")

    stats = matched_user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])

    counts = {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0}
    submissions = {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0}

    for row in stats:
        difficulty = row["difficulty"]
        counts[difficulty] = row["count"]
        submissions[difficulty] = row["submissions"]

    total_solved = counts.get("All", 0)
    total_submissions = submissions.get("All", 0)

    acceptance_rate = None
    if total_submissions > 0:
        acceptance_rate = round((total_solved / total_submissions) * 100, 2)

    return LeetCodeProfile(
        username=username,
        total_solved=total_solved,
        easy_solved=counts.get("Easy", 0),
        medium_solved=counts.get("Medium", 0),
        hard_solved=counts.get("Hard", 0),
        acceptance_rate=acceptance_rate,
        contest_rating=contest_data.get("rating") if contest_data else None,
        contest_count=contest_data.get("attendedContestsCount", 0) if contest_data else 0,
        solved_problems=[],
        contests=[],
    )