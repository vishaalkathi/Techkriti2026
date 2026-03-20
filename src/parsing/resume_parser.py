from src.core.llm import call_llm_json
from .prompts import RESUME_PROMPT
from .utils import validate_and_fix
from .schema import RESUME_SCHEMA
import json

def parse_resume(resume_text):
    prompt = RESUME_PROMPT.format(resume_text=resume_text)

    raw_output = call_llm_json(prompt)
    data = validate_and_fix(raw_output, RESUME_SCHEMA)
    return data