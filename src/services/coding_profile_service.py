from __future__ import annotations

from typing import Any, Dict, Optional

from src.coding_profiles.codeforces.client import (
    fetch_user_info,
    fetch_user_rating,
    fetch_user_status,
)
from src.coding_profiles.codeforces.parser import parse_codeforces_profile
from src.coding_profiles.codeforces.analyzer import analyze_codeforces

from src.coding_profiles.leetcode.client import fetch_leetcode_profile_data
from src.coding_profiles.leetcode.parser import parse_leetcode_profile
from src.coding_profiles.leetcode.analyzer import analyze_leetcode


def analyze_codeforces_handle(handle: str) -> Dict[str, Any]:
    """
    Fetch, parse, and analyze a Codeforces profile.
    """
    info_data = fetch_user_info(handle)
    rating_data = fetch_user_rating(handle)
    status_data = fetch_user_status(handle)

    profile = parse_codeforces_profile(
        handle=handle,
        info_data=info_data,
        rating_data=rating_data,
        status_data=status_data,
    )

    return analyze_codeforces(profile)


def analyze_leetcode_username(username: str) -> Dict[str, Any]:
    """
    Fetch, parse, and analyze a LeetCode profile.
    """
    raw_data = fetch_leetcode_profile_data(username)
    profile = parse_leetcode_profile(username=username, data=raw_data)
    return analyze_leetcode(profile)


def analyze_coding_profiles(
    codeforces_handle: Optional[str] = None,
    leetcode_username: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main entry point used by UI/app layer.

    Returns a combined dictionary with:
    - codeforces analysis
    - leetcode analysis
    - summary block
    """
    result: Dict[str, Any] = {
        "codeforces": None,
        "leetcode": None,
        "summary": {
            "platforms_analyzed": [],
            "strengths": [],
            "weaknesses": [],
        },
    }

    if codeforces_handle:
        try:
            cf_result = analyze_codeforces_handle(codeforces_handle)
            result["codeforces"] = cf_result
            result["summary"]["platforms_analyzed"].append("codeforces")
        except Exception as e:
            result["codeforces"] = {
                "error": f"Failed to analyze Codeforces handle '{codeforces_handle}': {str(e)}"
            }

    if leetcode_username:
        try:
            lc_result = analyze_leetcode_username(leetcode_username)
            result["leetcode"] = lc_result
            result["summary"]["platforms_analyzed"].append("leetcode")
        except Exception as e:
            result["leetcode"] = {
                "error": f"Failed to analyze LeetCode username '{leetcode_username}': {str(e)}"
            }

    result["summary"]["strengths"], result["summary"]["weaknesses"] = generate_summary_insights(
        result.get("codeforces"),
        result.get("leetcode"),
    )

    result["summary"]["overall_score"] = compute_overall_score(
        result.get("codeforces"),
        result.get("leetcode"),
    )

    return result


def generate_summary_insights(
    codeforces_data: Optional[Dict[str, Any]],
    leetcode_data: Optional[Dict[str, Any]],
) -> tuple[list[str], list[str]]:
    strengths: list[str] = []
    weaknesses: list[str] = []

    if codeforces_data and "error" not in codeforces_data:
        current_rating = codeforces_data.get("current_rating") or 0
        hardest_solved = codeforces_data.get("hardest_solved") or 0
        total_solved = codeforces_data.get("total_solved") or 0

        if current_rating >= 1400:
            strengths.append("Good competitive programming performance on Codeforces")
        elif current_rating > 0:
            weaknesses.append("Codeforces rating is still developing")

        if hardest_solved >= 1800:
            strengths.append("Has solved relatively difficult Codeforces problems")

        if total_solved >= 200:
            strengths.append("Good Codeforces problem-solving volume")
        elif total_solved > 0:
            weaknesses.append("Codeforces solved-problem volume is still limited")

    if leetcode_data and "error" not in leetcode_data:
        total_solved = leetcode_data.get("total_solved") or 0
        medium_solved = leetcode_data.get("medium_solved") or 0
        hard_solved = leetcode_data.get("hard_solved") or 0
        contest_rating = leetcode_data.get("contest_rating") or 0
        contest_count = leetcode_data.get("contest_count") or 0

        if total_solved >= 250:
            strengths.append("Strong LeetCode practice volume")
        elif total_solved > 0:
            weaknesses.append("LeetCode practice volume can improve")

        if medium_solved >= 100:
            strengths.append("Good medium-level DSA exposure on LeetCode")

        if hard_solved >= 40:
            strengths.append("Good hard-problem exposure on LeetCode")
        elif total_solved > 0:
            weaknesses.append("Limited hard-problem exposure on LeetCode")

        if contest_rating >= 1700:
            strengths.append("Strong LeetCode contest performance")
        elif contest_count > 0 and contest_rating < 1500:
            weaknesses.append("LeetCode contest performance is still developing")

    if not strengths:
        strengths.append("Profile data collected successfully")

    return strengths, weaknesses


def compute_overall_score(
    codeforces_data: Optional[Dict[str, Any]],
    leetcode_data: Optional[Dict[str, Any]],
) -> float:
    scores = []

    if codeforces_data and "error" not in codeforces_data:
        scores.append(score_codeforces(codeforces_data))

    if leetcode_data and "error" not in leetcode_data:
        scores.append(score_leetcode(leetcode_data))

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 2)


def score_codeforces(data: Dict[str, Any]) -> float:
    score = 0.0

    rating = data.get("current_rating") or 0
    solved = data.get("total_solved") or 0
    avg_solved_rating = data.get("avg_solved_rating") or 0
    contest_count = data.get("contest_count") or 0

    score += min(rating / 50, 40)              # up to 40
    score += min(solved / 10, 20)              # up to 20
    score += min(avg_solved_rating / 100, 20)  # up to 20
    score += min(contest_count / 2, 20)        # up to 20

    return round(score, 2)


def score_leetcode(data: Dict[str, Any]) -> float:
    score = 0.0

    total = data.get("total_solved") or 0
    medium = data.get("medium_solved") or 0
    hard = data.get("hard_solved") or 0
    contest_rating = data.get("contest_rating") or 0
    contest_count = data.get("contest_count") or 0

    score += min(total / 15, 25)           # up to 25
    score += min(medium / 5, 20)           # up to 20
    score += min(hard / 2, 25)             # up to 25
    score += min(contest_rating / 100, 20) # up to 20
    score += min(contest_count, 10)        # up to 10

    return round(score, 2)