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
# 🔹 SCORING HELPERS
# -------------------------------

def score_complexity(avg_complexity):
    """
    Lower complexity = better score
    Typical range: 1–10
    """
    if avg_complexity == 0:
        return 50  # neutral if no data

    score = max(0, 100 - (avg_complexity * 10))
    return min(score, 100)


def score_maintainability(avg_mi):
    """
    MI is already 0–100
    """
    return max(0, min(avg_mi, 100))


def score_linting(error_count, file_count):
    """
    Normalize errors per file
    """
    if file_count == 0:
        return 50

    errors_per_file = error_count / file_count

    score = max(0, 100 - (errors_per_file * 20))
    return min(score, 100)


# -------------------------------
# 🔹 FULL REPO QUALITY
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

    if file_count == 0:
        return 0

    avg_complexity = total_complexity / file_count
    avg_mi = total_mi / file_count

    flake_errors = analyze_flake8(repo_path)

    # -------------------------------
    # 🔹 COMPONENT SCORES
    # -------------------------------

    complexity_score = score_complexity(avg_complexity)
    mi_score = score_maintainability(avg_mi)
    lint_score = score_linting(flake_errors, file_count)

    # -------------------------------
    # 🔹 FINAL WEIGHTED SCORE
    # -------------------------------

    final_score = (
        0.3 * complexity_score +
        0.4 * mi_score +
        0.3 * lint_score
    )

    return round(final_score, 2)