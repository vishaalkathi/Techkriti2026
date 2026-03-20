import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import matplotlib.pyplot as plt
import streamlit as st

from src.services.coding_profile_service import analyze_coding_profiles

st.set_page_config(
    page_title="Coding Profile Analyzer",
    page_icon="💻",
    layout="wide",
)


def safe_number(value: Any, default: Any = "N/A") -> Any:
    if value is None:
        return default
    return value


def format_float(value: Optional[float], digits: int = 2) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}"


def score_band(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Strong"
    if score >= 50:
        return "Moderate"
    if score > 0:
        return "Developing"
    return "Unavailable"


def draw_leetcode_split_chart(lc_data: Dict[str, Any]) -> None:
    easy = lc_data.get("easy_solved", 0) or 0
    medium = lc_data.get("medium_solved", 0) or 0
    hard = lc_data.get("hard_solved", 0) or 0

    labels = ["Easy", "Medium", "Hard"]
    values = [easy, medium, hard]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values)
    ax.set_title("LeetCode Difficulty Split")
    ax.set_ylabel("Problems Solved")
    st.pyplot(fig)


def draw_codeforces_rating_bucket_chart(cf_data: Dict[str, Any]) -> None:
    buckets = cf_data.get("rating_bucket_breakdown", {}) or {}
    if not buckets:
        st.info("No Codeforces rating bucket data available.")
        return

    ordered_keys = [
        "<1200",
        "1200-1399",
        "1400-1599",
        "1600-1799",
        "1800-1999",
        "2000+",
        "unrated",
    ]
    labels = [k for k in ordered_keys if k in buckets]
    values = [buckets[k] for k in labels]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_title("Codeforces Solved Problems by Rating Bucket")
    ax.set_ylabel("Problems Solved")
    ax.set_xlabel("Problem Rating Bucket")
    plt.xticks(rotation=20)
    st.pyplot(fig)


def draw_codeforces_tag_chart(cf_data: Dict[str, Any]) -> None:
    tag_breakdown = cf_data.get("tag_breakdown", {}) or {}
    if not tag_breakdown:
        st.info("No Codeforces tag data available.")
        return

    top_items = list(tag_breakdown.items())[:8]
    labels = [item[0] for item in top_items]
    values = [item[1] for item in top_items]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_title("Top Codeforces Tags")
    ax.set_ylabel("Solved Count")
    ax.set_xlabel("Tags")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)


def draw_overall_platform_comparison(
    cf_data: Optional[Dict[str, Any]],
    lc_data: Optional[Dict[str, Any]],
) -> None:
    labels = []
    values = []

    if cf_data and "error" not in cf_data:
        labels.append("Codeforces Solved")
        values.append(cf_data.get("total_solved", 0) or 0)

    if lc_data and "error" not in lc_data:
        labels.append("LeetCode Solved")
        values.append(lc_data.get("total_solved", 0) or 0)

    if not labels:
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values)
    ax.set_title("Platform Problem-Solving Volume")
    ax.set_ylabel("Problems Solved")
    st.pyplot(fig)


def render_summary_cards(summary: Dict[str, Any]) -> None:
    overall_score = summary.get("overall_score", 0.0) or 0.0
    platforms = summary.get("platforms_analyzed", []) or []
    band = score_band(overall_score)

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Score", format_float(overall_score))
    c2.metric("Score Band", band)
    c3.metric("Platforms Analyzed", len(platforms))


def render_strengths_weaknesses(summary: Dict[str, Any]) -> None:
    strengths = summary.get("strengths", []) or []
    weaknesses = summary.get("weaknesses", []) or []

    left, right = st.columns(2)

    with left:
        st.markdown("### Strengths")
        if strengths:
            for item in strengths:
                st.success(item)
        else:
            st.info("No strengths generated.")

    with right:
        st.markdown("### Weaknesses")
        if weaknesses:
            for item in weaknesses:
                st.warning(item)
        else:
            st.info("No weaknesses generated.")


def render_codeforces_section(cf_data: Dict[str, Any]) -> None:
    st.subheader("Codeforces")

    if "error" in cf_data:
        st.error(cf_data["error"])
        return

    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    r1c1.metric("Current Rating", safe_number(cf_data.get("current_rating")))
    r1c2.metric("Max Rating", safe_number(cf_data.get("max_rating")))
    r1c3.metric("Total Solved", safe_number(cf_data.get("total_solved")))
    r1c4.metric("Contest Count", safe_number(cf_data.get("contest_count")))

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    r2c1.metric("Rank", safe_number(cf_data.get("rank")))
    r2c2.metric("Max Rank", safe_number(cf_data.get("max_rank")))
    r2c3.metric("Avg Solved Rating", format_float(cf_data.get("avg_solved_rating")))
    r2c4.metric("Hardest Solved", safe_number(cf_data.get("hardest_solved")))

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        draw_codeforces_rating_bucket_chart(cf_data)

    with chart_col2:
        draw_codeforces_tag_chart(cf_data)

    with st.expander("View full Codeforces data"):
        st.json(cf_data)


def render_leetcode_section(lc_data: Dict[str, Any]) -> None:
    st.subheader("LeetCode")

    if "error" in lc_data:
        st.error(lc_data["error"])
        return

    r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)
    r1c1.metric("Total Solved", safe_number(lc_data.get("total_solved")))
    r1c2.metric("Easy", safe_number(lc_data.get("easy_solved")))
    r1c3.metric("Medium", safe_number(lc_data.get("medium_solved")))
    r1c4.metric("Hard", safe_number(lc_data.get("hard_solved")))
    r1c5.metric("Contest Rating", format_float(lc_data.get("contest_rating")))

    r2c1, r2c2, r2c3 = st.columns(3)
    r2c1.metric("Acceptance Rate", format_float(lc_data.get("acceptance_rate")))
    r2c2.metric("Contest Attempts", safe_number(lc_data.get("contest_count")))

    hard_ratio = 0.0
    total_solved = lc_data.get("total_solved", 0) or 0
    hard_solved = lc_data.get("hard_solved", 0) or 0
    if total_solved > 0:
        hard_ratio = (hard_solved / total_solved) * 100
    r2c3.metric("Hard Ratio %", format_float(hard_ratio))

    draw_leetcode_split_chart(lc_data)

    with st.expander("View full LeetCode data"):
        st.json(lc_data)


st.title("💻 Coding Profile Analyzer")
st.caption("Analyze Codeforces and LeetCode profiles with metrics, charts, and summary insights.")

with st.sidebar:
    st.header("Inputs")
    cf_handle = st.text_input("Codeforces Handle", placeholder="e.g. tourist")
    lc_username = st.text_input("LeetCode Username", placeholder="e.g. some_user")
    analyze_button = st.button("Analyze Profiles")

    st.markdown("---")
    st.markdown("### Notes")
    st.write("- Enter one or both profiles.")
    st.write("- LeetCode acceptance rate may differ from the profile UI depending on source fields.")
    st.write("- Codeforces analysis includes solved counts, ratings, buckets, and top tags.")

if analyze_button:
    if not cf_handle and not lc_username:
        st.warning("Please enter at least one profile.")
    else:
        with st.spinner("Fetching and analyzing profiles..."):
            result = analyze_coding_profiles(
                codeforces_handle=cf_handle or None,
                leetcode_username=lc_username or None,
            )

        summary = result.get("summary", {}) or {}
        cf_data = result.get("codeforces")
        lc_data = result.get("leetcode")

        st.markdown("## Summary")
        render_summary_cards(summary)
        render_strengths_weaknesses(summary)

        st.markdown("## Platform Comparison")
        draw_overall_platform_comparison(cf_data, lc_data)

        if cf_data:
            st.markdown("---")
            render_codeforces_section(cf_data)

        if lc_data:
            st.markdown("---")
            render_leetcode_section(lc_data)

        with st.expander("View full combined result"):
            st.json(result)
else:
    st.info("Enter a Codeforces handle or LeetCode username in the sidebar, then click Analyze Profiles.")