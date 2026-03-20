import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import altair as alt
import pandas as pd



import tempfile

def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

from src.matching.skill_matcher import match_skills
from src.scoring.hybrid_scoring import calculate_score
from src.explanation.report_generator import generate_report
from src.parsing.profile_analytics_builder import build_profile_analytics
from src.parsing.profile_builder import build_profile

from src.analysis.skill_evidence import build_skill_evidence
from src.explanation.report_generator import generate_skill_reasoning


st.title("HireX Candidate Analyzer")
st.info("Fill details and click 'Analyze Candidate' to see results.")
if st.button("Go to Coding Profile Analyzer"):
    st.switch_page("pages/main.py")  



job_text = st.text_area("Paste Job Description")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


github_username = st.text_input("GitHub Username")
leetcode_username = st.text_input("LeetCode Username")
codeforces_handle = st.text_input("Codeforces Handle")

st.session_state["github"] = github_username
st.session_state["leetcode_username"] = leetcode_username
st.session_state["codeforces_handle"] = codeforces_handle

if st.button("Analyze Candidate"):

    if not job_text or not resume_file:
        st.warning("Please provide both job description and resume.")
    else:
        # Save resume
        resume_path = save_uploaded_file(resume_file)

        # Extract skills
        profile = build_profile(resume_path, job_text)

        resume_data = profile["resume"]
        jd_data = profile["job_description"]

        resume_skills = resume_data["skills"]

        # Combine required + preferred
        job_skills = jd_data["required_skills"] + jd_data["preferred_skills"]
        candidate_name = leetcode_username or github_username or "Candidate"

        candidate_profile = {
            "github_username": github_username or resume_data["github_username"],
            "leetcode_username": leetcode_username or resume_data["leetcode_username"],
            "codeforces_handle": codeforces_handle or resume_data["codeforces_handle"]
        }

        with st.spinner("Analyzing candidate profiles..."):
            try:
                candidate_data = build_profile_analytics(candidate_profile)
               
                skill_evidence = build_skill_evidence(resume_skills, candidate_data)
            except Exception as e:
                st.error(f"Failed to fetch profile data: {e}")
                candidate_data = {}
                skill_evidence = {}
        github_skills = candidate_data.get("github_top_languages", [])

        # Combine Resume + GitHub skills
        candidate_skills_combined = list(set(resume_skills + github_skills))

        # Skill matching
        print("JOB SKILLS:", job_skills)
        print("CANDIDATE SKILLS:", candidate_skills_combined)
        skill_results = match_skills(candidate_skills_combined, job_skills)

        # Hybrid scoring
        total_score_dict = calculate_score(
            candidate_data,
            skill_results,
            skill_evidence,
            resume_data,
            jd_data
        )

        breakdown = total_score_dict["breakdown"]

        df = pd.DataFrame({
            "Category": list(breakdown.keys()),
            "Score": list(breakdown.values())
        })

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Category", sort=None),
            y=alt.Y("Score")
        )

        

        report_dict, paragraph = generate_report(candidate_name, skill_results, total_score_dict,skill_evidence)
        evidence_lines = []

        
        st.subheader("Skill Evidence Breakdown")

        for skill, ev in skill_evidence.items():
            st.write(f"### {skill}")
            st.write(f"- Repos: {ev['repo_count']}")
            st.write(f"- Recent: {ev['recent_activity']}")
            st.write(f"- Project Types: {', '.join(ev['project_types'])}")
            st.write(f"- Confidence: {ev['confidence']}")
        st.subheader("Skill Evidence Reasoning")

        for skill in report_dict["skill_matching"]["matched_skills"]:
            ev = skill_evidence.get(skill, {})
            reasoning = generate_skill_reasoning(skill, ev)
            st.write(f"• {reasoning}")
            
        st.subheader("Candidate Fit Summary")
        st.write(paragraph)

        st.subheader("Matched Skills")
        st.write(", ".join(report_dict["skill_matching"]["matched_skills"]))
        st.subheader("Missing Skills")
        st.write(", ".join(report_dict["skill_matching"]["missing_skills"]))
        st.subheader("Score")
        st.metric("Total Score", total_score_dict["total_score"])

        st.subheader("Score Breakdown Visualization")
        st.altair_chart(chart)

        if st.button("🔍 View Coding Profile Insights"):
            st.switch_page("pages/main.py")