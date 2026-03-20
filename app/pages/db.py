import sys
import os

# Fix import issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.github_analyzer.analyzer import analyze_github_profile

st.title("🚀 GitHub Profile Analyzer")

# Input
username = st.text_input("Enter GitHub Username")

# Button
if st.button("Analyze"):
    if not username:
        st.warning("Please enter a username")
    else:
        st.write("Analyzing...")

        result = analyze_github_profile(username)
        st.write("DEBUG RESULT:", result)

        if not result:
            st.error("No data found or API error")
        else:
            st.success("Analysis Complete ✅")

            # Basic Info
            st.subheader("📊 Basic Info")
            st.write(result.get("basic_info", {}))

            # Languages
            st.subheader("💻 Languages")
            st.write(result.get("languages", {}))

            # Top Repos
            st.subheader("⭐ Top Repositories")
            top_repos = result.get("top_repos", [])

            for repo in top_repos:
                st.write(f"{repo['name']} - ⭐ {repo['stargazers_count']}")