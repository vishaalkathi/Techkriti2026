import fitz
import re
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(_file_), "../../"))
SKILLS_PATH = os.path.join(BASE_DIR, "data", "skills_dataset.txt")

def load_skills(file_path=SKILLS_PATH):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Skills file not found at: {file_path}")
    skills = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = line.strip().lower()
            if cleaned_line:
                skills.append(cleaned_line)
    return skills

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text() + " "
    text = re.sub(r"\s+", " ", text)
    return text.lower()

def extract_candidate_phrases(text):
    skills_db = load_skills()
    found = []
    for skill in skills_db:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found.append(skill)
    return list(set(found))

def extract_resume_skills(file_path):
    text = extract_text_from_pdf(file_path)
    return extract_candidate_phrases(text)

def extract_candidate_ids(file_path):
    text = extract_text_from_pdf(file_path)
    candidate_ids = {}

    github_id = re.search(r"github\.com/([A-Za-z0-9_-]+)", text)
    if github_id: candidate_ids["github"] = github_id.group(1)

    leetcode_id = re.search(r"leetcode\.com/([A-Za-z0-9_-]+)", text)
    if leetcode_id: candidate_ids["leetcode"] = leetcode_id.group(1)

    codeforces_id = re.search(r"codeforces\.com/profile/([A-Za-z0-9_-]+)", text)
    if codeforces_id: candidate_ids["codeforces"] = codeforces_id.group(1)

    return candidate_ids

def extract_name(file_path):
    text = extract_text_from_pdf(file_path)
    lines = text.split("\n")
    for line in lines:
        if len(line.split()) <= 3 and all(w[0].isupper() for w in line.split() if w):
            return line.strip()
    return "Candidate"