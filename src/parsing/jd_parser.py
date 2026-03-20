from src.core.llm import call_llm_json
from .prompts import JD_PROMPT
from .utils import validate_and_fix
from .schema import JD_SCHEMA
from .spacy_extractor import extract_skills_spacy
import json

def parse_jd(jd_text):
    prompt = JD_PROMPT.format(jd_text=jd_text)

    raw_output = call_llm_json(prompt)
    data = validate_and_fix(raw_output, JD_SCHEMA)

    if not data.get("required_skills"):
        fallback_skills = extract_skills_spacy(jd_text)
        data["required_skills"] = fallback_skills
    return data