import re
import fitz

def extract_text_from_pdf(file_path):
    # get text from resume pdf
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            content = page.get_text()
            if content:
                text += content + " "
    
    text = re.sub(r"\s+", " ", text)
    return text.lower()