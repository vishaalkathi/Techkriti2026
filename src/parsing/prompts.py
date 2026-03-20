RESUME_PROMPT = """
You are an expert resume parser.

Extract structured information from the resume.

Return ONLY valid JSON (no explanation, no extra text).

Schema:
{
  "skills": list of strings,
  "projects": list of strings,
  "experience_years": integer,
  "education": string,

  "github_username": string,
  "leetcode_username": string,
  "codeforces_handle": string
}

Instructions:

1. Extract ALL technical skills (programming, frameworks, tools).
2. Extract 1-5 key projects (short names only).
3. Estimate total years of experience (integer).
4. Extract highest education.

5. Extract usernames from:
   - URLs like:
     https://github.com/username
     https://leetcode.com/username
     https://codeforces.com/profile/username
   - OR plain text mentions

6. If a username is missing → return empty string "".

7. If any field is missing:
   - skills → []
   - projects → []
   - experience_years → 0
   - education → ""

Resume:
{resume_text}
"""

JD_PROMPT = """
You are an expert job description analyzer.

Extract structured hiring requirements.

Return ONLY valid JSON (no explanation).

Schema:
{
  "required_skills": list of strings,
  "preferred_skills": list of strings,
  "experience_required": integer
}

Instructions:

1. Extract MUST-HAVE skills → required_skills
2. Extract GOOD-TO-HAVE skills → preferred_skills
3. Extract experience requirement (integer years)

4. If experience is not mentioned → 0

5. Normalize skills (e.g., "Python", "Machine Learning")

Job Description:
{jd_text}
"""