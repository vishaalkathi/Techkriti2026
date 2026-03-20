from src.parsing.text_extractor import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.parsing.jd_parser import parse_jd


def build_profile(resume_file, jd_text):
    # Step 1: extract raw text
    resume_text = extract_text_from_pdf(resume_file)

    # Step 2: parse
    resume_data = parse_resume(resume_text)
    jd_data = parse_jd(jd_text)

    # Step 3: combine
    profile = {
        "resume": resume_data,
        "job_description": jd_data
    }

    return profile