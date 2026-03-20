import subprocess
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import os


# -------------------------------
# 🔹 RADON ANALYSIS
# -------------------------------

def analyze_radon(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        complexity_blocks = cc_visit(code)
        mi = mi_visit(code, multi=True)

        avg_complexity = (
            sum(block.complexity for block in complexity_blocks) / len(complexity_blocks)
            if complexity_blocks else 0
        )

        return avg_complexity, mi

    except Exception:
        return 0, 0


# -------------------------------
# 🔹 FLAKE8 ANALYSIS
# -------------------------------

def analyze_flake8(repo_path):
    try:
        result = subprocess.run(
            ["flake8", repo_path],
            capture_output=True,
            text=True
        )

        errors = result.stdout.splitlines()
        return len(errors)

    except Exception:
        return 0


# -------------------------------
# 🔹 FULL REPO QUALITY (FINAL)
# -------------------------------

def analyze_repo_code_quality(repo_path):
    total_complexity = 0
    total_mi = 0
    file_count = 0

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)

                complexity, mi = analyze_radon(path)

                total_complexity += complexity
                total_mi += mi
                file_count += 1

    # If no Python files found
    if file_count == 0:
        return {
            "avg_complexity": 0,
            "maintainability_index": 0,
            "flake8_issues": 0
        }

    avg_complexity = total_complexity / file_count
    avg_mi = total_mi / file_count

    flake_errors = analyze_flake8(repo_path)

    return {
        "avg_complexity": round(avg_complexity, 2),
        "maintainability_index": round(avg_mi, 2),
        "flake8_issues": flake_errors
    }