from src.core.llm import call_llm_json
from .prompts import RESUME_PROMPT
from .utils import validate_and_fix
from .schema import RESUME_SCHEMA
from .spacy_extractor import extract_skills_spacy
import json

def parse_resume(resume_text):
    prompt = RESUME_PROMPT.format(resume_text=resume_text)

    raw_output = call_llm_json(prompt)
    data = validate_and_fix(raw_output, RESUME_SCHEMA)

    if not data.get("skills"):
        fallback_skills = extract_skills_spacy(resume_text)
        data["skills"] = fallback_skills
    return data