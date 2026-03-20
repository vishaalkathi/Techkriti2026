import spacy
import re
from .skills_dataset import SKILLS_DB

nlp = spacy.load("en_core_web_sm")


def extract_skills_spacy(text):
    text = text.lower()
    doc = nlp(text)

    found_skills = set()
    candidates = set()

    for ent in doc.ents:
        candidates.add(ent.text.strip())

    for chunk in doc.noun_chunks:
        candidates.add(chunk.text.strip())

    for token in doc:
        if not token.is_stop and not token.is_punct:
            candidates.add(token.text.strip())

    for candidate in candidates:
        for canonical, aliases in SKILLS_DB.items():
            for alias in aliases:
                if re.fullmatch(rf"{re.escape(alias)}", candidate):
                    found_skills.add(canonical)

    return list(found_skills)

def extract_candidate_ids(text):
    candidate_ids = {}

    github_pattern = r"github\.com/([A-Za-z0-9_-]+)"
    github_id = re.search(github_pattern, text)
    if github_id:
        candidate_ids["github"] = github_id.group(1)

    leetcode_pattern = r"leetcode\.com/([A-Za-z0-9_-]+)"
    leetcode_id = re.search(leetcode_pattern, text)
    if leetcode_id:
        candidate_ids["leetcode"] = leetcode_id.group(1)

    codeforces_pattern = r"codeforces\.com/profile/([A-Za-z0-9_-]+)"
    codeforces_id = re.search(codeforces_pattern, text)
    if codeforces_id:
        candidate_ids["codeforces"] = codeforces_id.group(1)

    return candidate_ids