import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import tempfile

# -----------------------------
# 🔹 IMPORTS (YOUR PIPELINE)
# -----------------------------
from src.matching.skill_matcher import match_skills
from src.scoring.hybrid_scoring import calculate_score
from src.explanation.report_generator import generate_report, generate_skill_reasoning
from src.parsing.profile_analytics_builder import build_profile_analytics
from src.parsing.profile_builder import build_profile
from src.analysis.skill_evidence import build_skill_evidence
from src.parsing.resume_parser import load_skills, extract_text_from_pdf, extract_resume_skills, extract_candidate_ids

# -----------------------------
# 🔹 PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="HireX Analyzer", layout="wide")

st.title("🚀 HireX Candidate Analyzer")

# -----------------------------
# 🔹 FILE SAVE
# -----------------------------
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

# -----------------------------
# 🔹 GAUGE FUNCTION (NEW 🔥)
# -----------------------------
def gauge_chart(title, value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"},
            ],
        }
    ))
    return fig

# -----------------------------
# 🔹 INPUTS
# -----------------------------
job_text = st.text_area("📄 Paste Job Description")
resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])

github_username = st.text_input("GitHub Username")
leetcode_username = st.text_input("LeetCode Username")
codeforces_handle = st.text_input("Codeforces Handle")

st.session_state["github"] = github_username
st.session_state["leetcode_username"] = leetcode_username
st.session_state["codeforces_handle"] = codeforces_handle

# -----------------------------
# 🔹 MAIN BUTTON
# -----------------------------
if st.button("🔍 Analyze Candidate"):

    if not job_text or not resume_file:
        st.warning("Please provide both job description and resume.")
        st.stop()

    # Save resume
    resume_path = save_uploaded_file(resume_file)

    # -----------------------------
    # 🔹 PROFILE BUILDING
    # -----------------------------
    profile = build_profile(resume_path, job_text)

    resume_data = profile["resume"]
    jd_data = profile["job_description"]

    resume_skills = resume_data.get("skills", [])

    job_skills = jd_data.get("required_skills", []) + jd_data.get("preferred_skills", [])

    candidate_name = leetcode_username or github_username or "Candidate"

    candidate_profile = {
        "github_username": github_username or resume_data.get("github_username"),
        "leetcode_username": leetcode_username or resume_data.get("leetcode_username"),
        "codeforces_handle": codeforces_handle or resume_data.get("codeforces_handle")
    }

    # -----------------------------
    # 🔹 ANALYTICS FETCH
    # -----------------------------
    with st.spinner("Analyzing profiles..."):
        try:
            candidate_data = build_profile_analytics(candidate_profile)
            skill_evidence = build_skill_evidence(resume_skills, candidate_data)
        except Exception as e:
            st.error(f"Failed to fetch profile data: {e}")
            candidate_data = {}
            skill_evidence = {}

    github_skills = candidate_data.get("github_top_languages", [])

    candidate_skills_combined = list(set(resume_skills + github_skills))

    # -----------------------------
    # 🔹 SKILL MATCHING
    # -----------------------------
    skill_results = match_skills(candidate_skills_combined, job_skills)

    # -----------------------------
    # 🔹 SCORING
    # -----------------------------
    total_score_dict = calculate_score(
        candidate_data,
        skill_results,
        skill_evidence,
        resume_data,
        jd_data
    )

    total_score = total_score_dict.get("total_score", 0)
    breakdown = total_score_dict.get("breakdown", {})

    # -----------------------------
    # 🔥 SCORE GAUGE (NEW)
    # -----------------------------
    st.subheader("🏆 Candidate Score")

    st.plotly_chart(gauge_chart("Overall Score", total_score), use_container_width=True)

    # -----------------------------
    # 🔹 BAR CHART
    # -----------------------------
    df = pd.DataFrame({
        "Category": list(breakdown.keys()),
        "Score": list(breakdown.values())
    })

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category", sort=None),
        y="Score"
    )

    st.subheader("📊 Score Breakdown")
    st.altair_chart(chart, use_container_width=True)

    # -----------------------------
    # 🔹 REPORT
    # -----------------------------
    report_dict, paragraph = generate_report(
        candidate_name,
        skill_results,
        total_score_dict,
        skill_evidence
    )

    st.subheader("🧠 Candidate Summary")
    st.info(paragraph)

    # -----------------------------
    # 🔹 SKILL MATCH
    # -----------------------------
    st.subheader("✅ Matched Skills")
    st.write(", ".join(report_dict["skill_matching"]["matched_skills"]))

    st.subheader("❌ Missing Skills")
    st.write(", ".join(report_dict["skill_matching"]["missing_skills"]))

    # -----------------------------
    # 🔹 SKILL EVIDENCE
    # -----------------------------
    st.subheader("📂 Skill Evidence")

    for skill, ev in skill_evidence.items():
        st.markdown(f"### {skill}")
        st.write(f"Repos: {ev.get('repo_count', 0)}")
        st.write(f"Recent Activity: {ev.get('recent_activity', 0)}")
        st.write(f"Confidence: {ev.get('confidence', 0)}")

    # -----------------------------
    # 🔹 AI REASONING
    # -----------------------------
    st.subheader("🧠 Skill Reasoning")

    for skill in report_dict["skill_matching"]["matched_skills"]:
        ev = skill_evidence.get(skill, {})
        reasoning = generate_skill_reasoning(skill, ev)
        st.write(f"• {reasoning}")

    # -----------------------------
    # 🔹 NAVIGATION
    # -----------------------------
    if st.button("📊 View Coding Profile Insights"):
        st.switch_page("pages/main.py")