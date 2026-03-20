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