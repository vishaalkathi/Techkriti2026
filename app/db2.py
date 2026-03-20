import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# 🔹 IMPORTS
# -----------------------------
from src.github_analyzer.analyzer import analyze_github_profile
from src.services.coding_profile_service import analyze_coding_profiles
from src.scoring.profile_scoring import compute_profile_score
from src.ai.summary_generator import generate_profile_summary
from src.matching.skill_matcher import match_skills
from src.parsing.resume_parser import load_skills, extract_resume_skills

# -----------------------------
# 🔹 PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Dev Analyzer", layout="wide")
st.title("🚀 Developer Profile Analyzer")

# -----------------------------
# 🔹 SAVE FILE
# -----------------------------
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

# -----------------------------
# 🔹 GAUGE CHART
# -----------------------------
def gauge_chart(title, value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 10]},
            'steps': [
                {'range': [0, 4], 'color': "red"},
                {'range': [4, 7], 'color': "orange"},
                {'range': [7, 10], 'color': "green"},
            ],
        }
    ))
    return fig

# -----------------------------
# 🔥 SKILL TAG UI
# -----------------------------
def render_skill_tags(skills, color):
    if not skills:
        st.write("No data")
        return

    tags = ""
    for skill in skills:
        tags += f"""
        <span style="
            background-color:{color};
            color:white;
            padding:6px 12px;
            margin:4px;
            border-radius:12px;
            display:inline-block;
            font-size:14px;
        ">
        {skill}
        </span>
        """
    st.markdown(tags, unsafe_allow_html=True)

# -----------------------------
# 🔹 INPUTS
# -----------------------------
job_text = st.text_area("📄 Paste Job Description")
resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])

github_username = st.text_input("GitHub Username", "kennethreitz")
cf_handle = st.text_input("Codeforces Handle", "tourist")
lc_username = st.text_input("LeetCode Username", "leetcode")

# -----------------------------
# 🔥 MAIN BUTTON
# -----------------------------
if st.button("🔍 Analyze Candidate"):

    if not job_text or not resume_file:
        st.warning("Please provide both job description and resume.")
        st.stop()

    # Save resume
    resume_path = save_uploaded_file(resume_file)

    # -----------------------------
    # 🔹 RESUME + JD PROCESSING
    # -----------------------------
    with st.spinner("Processing resume..."):
        resume_skills = extract_resume_skills(resume_path)

    job_text_clean = job_text.lower().replace(",", " ")
    all_skills = load_skills()
    job_skills = [skill for skill in all_skills if skill in job_text_clean]

    if not job_skills:
        st.error("⚠️ No skills detected from job description.")
        st.stop()

    # -----------------------------
    # 🔹 PROFILE DATA
    # -----------------------------
    with st.spinner("Fetching profile data..."):

        github_data = analyze_github_profile(github_username)

        if "error" in github_data:
            st.error("Invalid GitHub username")
            st.stop()

        profile_analytics = github_data.get("profile_analytics", {})

        coding_data = analyze_coding_profiles(
            codeforces_handle=cf_handle,
            leetcode_username=lc_username
        )

        profile_analytics.update(coding_data)

    # -----------------------------
    # 🔹 SKILL MERGE
    # -----------------------------
    github_skills = profile_analytics.get("github_top_languages", [])
    candidate_skills = list(set(resume_skills + github_skills))

    skill_results = match_skills(candidate_skills, job_skills)

    # -----------------------------
    # 🔹 SCORING
    # -----------------------------
    scores = compute_profile_score(profile_analytics)
    profile_analytics.update(scores)

    summary = generate_profile_summary(profile_analytics)

    # -----------------------------
    # 🏆 SCORE
    # -----------------------------
    st.subheader("🏆 Score Overview")

    col1, col2, col3 = st.columns(3)

    col1.plotly_chart(gauge_chart("GitHub Score", scores.get("github_score", 0)), use_container_width=True)
    col2.plotly_chart(gauge_chart("Coding Score", scores.get("coding_score", 0)), use_container_width=True)
    col3.plotly_chart(gauge_chart("Overall Score", scores.get("overall_profile_score", 0)), use_container_width=True)

    # -----------------------------
    # 🧠 SUMMARY
    # -----------------------------
    st.subheader("🧠 AI Summary")
    st.info(summary)

    # -----------------------------
    # 🛠️ SKILLS UI (BEAUTIFUL)
    # -----------------------------
    st.subheader("🛠️ Skill Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Resume Skills")
        render_skill_tags(resume_skills, "#4CAF50")

    with col2:
        st.markdown("### 💻 GitHub Skills")
        render_skill_tags(github_skills, "#2196F3")

    st.markdown("### 📌 Job Skills")
    render_skill_tags(job_skills, "#9C27B0")

    # -----------------------------
    # ✅ MATCHING UI
    # -----------------------------
    matched = skill_results.get("matched_skills", [])
    missing = skill_results.get("missing_skills", [])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matched Skills")
        render_skill_tags(matched, "#2ECC71")

    with col2:
        st.markdown("### ❌ Missing Skills")
        render_skill_tags(missing, "#E74C3C")

    # -----------------------------
    # 📊 GITHUB METRICS
    # -----------------------------
    st.subheader("📊 GitHub Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Maintainability", profile_analytics.get("github_maintainability_index", "N/A"))
    col2.metric("Complexity", profile_analytics.get("github_avg_complexity", "N/A"))
    col3.metric("Flake8 Issues", profile_analytics.get("github_flake8_issues", "N/A"))

    # -----------------------------
    # ⚡ CODEFORCES
    # -----------------------------
    if profile_analytics.get("codeforces"):
        st.subheader("⚡ Codeforces")

        cf = profile_analytics["codeforces"]

        col1, col2 = st.columns(2)
        col1.metric("Rating", cf.get("current_rating"))
        col2.metric("Solved", cf.get("total_solved"))

    # -----------------------------
    # 🧩 LEETCODE
    # -----------------------------
    if profile_analytics.get("leetcode"):
        st.subheader("🧩 LeetCode")

        lc = profile_analytics["leetcode"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", lc.get("total_solved"))
        col2.metric("Medium", lc.get("medium_solved"))
        col3.metric("Hard", lc.get("hard_solved"))

        df = pd.DataFrame({
            "Difficulty": ["Easy", "Medium", "Hard"],
            "Count": [
                lc.get("easy_solved", 0),
                lc.get("medium_solved", 0),
                lc.get("hard_solved", 0)
            ]
        })

        st.bar_chart(df.set_index("Difficulty"))