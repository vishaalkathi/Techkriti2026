from src.coding_profiles.models import ProblemRecord, ContestRecord, CodeforcesProfile


def parse_codeforces_profile(handle: str, info_data: dict, rating_data: dict, status_data: dict) -> CodeforcesProfile:
    user = info_data["result"][0]

    contests = []
    for item in rating_data.get("result", []):
        contests.append(
            ContestRecord(
                contest_id=str(item["contestId"]),
                contest_name=item["contestName"],
                rank=item.get("rank"),
                old_rating=item.get("oldRating"),
                new_rating=item.get("newRating"),
                rating_change=(item.get("newRating", 0) - item.get("oldRating", 0))
                if item.get("newRating") is not None and item.get("oldRating") is not None
                else None,
                attended_at=item.get("ratingUpdateTimeSeconds"),
            )
        )

    solved_map = {}

    for sub in status_data.get("result", []):
        if sub.get("verdict") != "OK":
            continue

        problem = sub.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        if contest_id is None or index is None:
            continue

        pid = f"{contest_id}{index}"
        if pid not in solved_map:
            solved_map[pid] = ProblemRecord(
                platform="codeforces",
                problem_id=pid,
                title=problem.get("name", ""),
                rating=problem.get("rating"),
                topics=problem.get("tags", []),
                solved_at=sub.get("creationTimeSeconds"),
            )
        else:
            old_ts = solved_map[pid].solved_at
            new_ts = sub.get("creationTimeSeconds")
            if old_ts is None or (new_ts is not None and new_ts < old_ts):
                solved_map[pid].solved_at = new_ts

    solved_problems = list(solved_map.values())

    return CodeforcesProfile(
        handle=handle,
        current_rating=user.get("rating"),
        max_rating=user.get("maxRating"),
        rank=user.get("rank"),
        max_rank=user.get("maxRank"),
        total_solved=len(solved_problems),
        contests=contests,
        solved_problems=solved_problems,
    )