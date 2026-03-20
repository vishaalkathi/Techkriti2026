from src.github_analyzer.analyzer import analyze_github_profile
from src.scoring.profile_scoring import compute_profile_score
from src.services.coding_profile_service import analyze_coding_profiles

username = "torvalds"

result = analyze_github_profile(username)

if "error" in result:
    print("❌ Error:", result["error"])
else:
    profile_analytics = result["profile_analytics"]

    # 🔥 ADD CODING DATA
    coding_data = analyze_coding_profiles(
        codeforces_handle="tourist",
        leetcode_username="leetcode"
    )

    profile_analytics.update(coding_data)

    print("\n📊 PROFILE ANALYTICS:")
    print(profile_analytics)

    scores = compute_profile_score(profile_analytics)

    print("\n🏆 FINAL SCORES:")
    print(scores)