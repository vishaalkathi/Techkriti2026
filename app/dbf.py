import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.github_analyzer.analyzer import analyze_github_profile
from src.services.coding_profile_service import analyze_coding_profiles
from src.scoring.profile_scoring import compute_profile_score
from src.ai.summary_generator import generate_profile_summary


st.set_page_config(page_title="Dev Analyzer", layout="wide")

st.title("🚀 Developer Profile Analyzer")

# -----------------------------
# 🔹 INPUTS
# -----------------------------
github_username = st.text_input("GitHub Username", "kennethreitz")
cf_handle = st.text_input("Codeforces Handle", "tourist")
lc_username = st.text_input("LeetCode Username", "leetcode")


# -----------------------------
# 🔹 GAUGE CHART FUNCTION
# -----------------------------
def gauge_chart(title, value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [0, 4], 'color': "red"},
                {'range': [4, 7], 'color': "orange"},
                {'range': [7, 10], 'color': "green"},
            ],
        }
    ))
    return fig


# -----------------------------
# 🔹 MAIN BUTTON
# -----------------------------
if st.button("Analyze Profile"):

    with st.spinner("Analyzing profile..."):

        github_data = analyze_github_profile(github_username)

        if "error" in github_data:
            st.error("Invalid GitHub username")
            st.stop()

        profile_analytics = github_data["profile_analytics"]

        coding_data = analyze_coding_profiles(
            codeforces_handle=cf_handle,
            leetcode_username=lc_username
        )

        profile_analytics.update(coding_data)

        scores = compute_profile_score(profile_analytics)
        profile_analytics.update(scores)

        summary = generate_profile_summary(profile_analytics)

    # -----------------------------
    # 🔹 GAUGE SCORES
    # -----------------------------
    st.subheader("🏆 Score Overview")

    col1, col2, col3 = st.columns(3)

    col1.plotly_chart(gauge_chart("GitHub Score", scores["github_score"]), use_container_width=True)
    col2.plotly_chart(gauge_chart("Coding Score", scores["coding_score"]), use_container_width=True)
    col3.plotly_chart(gauge_chart("Overall Score", scores["overall_profile_score"]), use_container_width=True)

    # -----------------------------
    # 🔹 AI SUMMARY
    # -----------------------------
    st.subheader("🧠 AI Summary")
    st.info(summary)

    # -----------------------------
    # 🔹 GITHUB METRICS
    # -----------------------------
    st.subheader("📊 GitHub Insights")

    mi = profile_analytics.get("github_maintainability_index")
    complexity = profile_analytics.get("github_avg_complexity")
    flake = profile_analytics.get("github_flake8_issues")

    col1, col2, col3 = st.columns(3)

    col1.metric("Maintainability Index", mi if mi else "N/A")
    col2.metric("Avg Complexity", complexity if complexity else "N/A")
    col3.metric("Flake8 Issues", flake if flake else "N/A")

    st.write("Languages:", profile_analytics.get("github_top_languages", []))

    # -----------------------------
    # 🔹 CODEFORCES
    # -----------------------------
    if profile_analytics.get("codeforces"):
        st.subheader("⚡ Codeforces Insights")

        cf = profile_analytics["codeforces"]

        col1, col2 = st.columns(2)
        col1.metric("Rating", cf.get("current_rating"))
        col2.metric("Solved", cf.get("total_solved"))

        tag_data = cf.get("tag_breakdown", {})

        if tag_data:
            df = pd.DataFrame(list(tag_data.items()), columns=["Tag", "Count"])
            df = df.sort_values(by="Count", ascending=False).head(10)

            st.write("Top Problem Tags")
            st.bar_chart(df.set_index("Tag"))

    # -----------------------------
    # 🔹 LEETCODE
    # -----------------------------
    if profile_analytics.get("leetcode"):
        st.subheader("🧩 LeetCode Insights")

        lc = profile_analytics["leetcode"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", lc.get("total_solved"))
        col2.metric("Medium", lc.get("medium_solved"))
        col3.metric("Hard", lc.get("hard_solved"))

        lc_data = {
            "Easy": lc.get("easy_solved", 0),
            "Medium": lc.get("medium_solved", 0),
            "Hard": lc.get("hard_solved", 0),
        }

        df = pd.DataFrame(list(lc_data.items()), columns=["Difficulty", "Count"])
        st.bar_chart(df.set_index("Difficulty"))