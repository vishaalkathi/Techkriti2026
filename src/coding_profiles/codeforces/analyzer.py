from collections import Counter, defaultdict


def analyze_codeforces(profile):
    tag_counts = Counter()
    rating_buckets = {
        "<1200": 0,
        "1200-1399": 0,
        "1400-1599": 0,
        "1600-1799": 0,
        "1800-1999": 0,
        "2000+": 0,
        "unrated": 0,
    }

    ratings = []

    for prob in profile.solved_problems:
        for tag in prob.topics:
            tag_counts[tag] += 1

        if prob.rating is None:
            rating_buckets["unrated"] += 1
        else:
            ratings.append(prob.rating)
            if prob.rating < 1200:
                rating_buckets["<1200"] += 1
            elif prob.rating < 1400:
                rating_buckets["1200-1399"] += 1
            elif prob.rating < 1600:
                rating_buckets["1400-1599"] += 1
            elif prob.rating < 1800:
                rating_buckets["1600-1799"] += 1
            elif prob.rating < 2000:
                rating_buckets["1800-1999"] += 1
            else:
                rating_buckets["2000+"] += 1

    avg_solved_rating = sum(ratings) / len(ratings) if ratings else None
    hardest_solved = max(ratings) if ratings else None

    recent_contests = profile.contests[-5:] if profile.contests else []
    trend = None
    if len(recent_contests) >= 2:
        trend = recent_contests[-1].new_rating - recent_contests[0].new_rating

    return {
        "handle": profile.handle,
        "current_rating": profile.current_rating,
        "max_rating": profile.max_rating,
        "rank": profile.rank,
        "max_rank": profile.max_rank,
        "total_solved": profile.total_solved,
        "contest_count": len(profile.contests),
        "avg_solved_rating": avg_solved_rating,
        "hardest_solved": hardest_solved,
        "tag_breakdown": dict(tag_counts.most_common()),
        "rating_bucket_breakdown": rating_buckets,
        "recent_rating_trend": trend,
    }