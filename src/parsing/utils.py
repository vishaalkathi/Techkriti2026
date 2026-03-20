def normalize_skills(skills):
    return [skill.lower().strip() for skill in skills]

import re

def clean_username(value):

    if not value:
        return ""

    value = str(value).strip()

    # GitHub
    if "github.com" in value:
        return value.rstrip("/").split("/")[-1]

    # LeetCode
    if "leetcode.com" in value:
        return value.rstrip("/").split("/")[-1]

    # Codeforces
    if "codeforces.com" in value:
        return value.rstrip("/").split("/")[-1]

    value = re.sub(r"(github|leetcode|codeforces)[:\-\s]*", "", value, flags=re.I)

    value = re.sub(r"[^a-zA-Z0-9_\-]", "", value)

    return value.strip()


def validate_and_fix(data, schema):
    validated = {}

    for key, expected_type in schema.items():
        value = data.get(key)

        if value is None:
            if expected_type == list:
                validated[key] = []
            elif expected_type == int:
                validated[key] = 0
            elif expected_type == str:
                validated[key] = ""
            continue

        try:
            # LIST
            if expected_type == list:
                if isinstance(value, list):
                    validated[key] = value
                else:
                    validated[key] = [str(value)]

            # INT
            elif expected_type == int:
                if isinstance(value, int):
                    validated[key] = value
                else:
                    num = re.findall(r"\d+", str(value))
                    validated[key] = int(num[0]) if num else 0

            elif expected_type == str:

                if key in ["github_username", "leetcode_username", "codeforces_handle"]:
                    validated[key] = clean_username(value)

                else:
                    validated[key] = str(value).strip()

        except:
            # fallback
            if expected_type == list:
                validated[key] = []
            elif expected_type == int:
                validated[key] = 0
            elif expected_type == str:
                validated[key] = ""

    return validated