from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize_skills(skills):
    if not skills:
        return []
    return [skill.strip().lower() for skill in skills]


def embed_skills(skills):
    return model.encode(skills)


def match_skills(candidate_skills, job_skills, min_similarity=0.8):

    # ✅ Normalize
    candidate_skills = normalize_skills(candidate_skills)
    job_skills = normalize_skills(job_skills)

    # ✅ Handle empty case
    if not candidate_skills or not job_skills:
        return {
            "matched": [],
            "missing": job_skills,
            "match_count": 0,
            "total_required": len(job_skills),
            "match_percentage": 0
        }

    candidate_embeddings = embed_skills(candidate_skills)
    job_embeddings = embed_skills(job_skills)
    

    matched = []
    missing = []

    total_score = 0
    candidate_set = set(candidate_skills)

    for i, job_vec in enumerate(job_embeddings):

        job_skill = job_skills[i]

        # ✅ Exact match (priority)
        if job_skill in candidate_set:
            matched.append(job_skill)
            total_score += 1
            continue

        # ✅ Semantic match
        similarity_scores = cosine_similarity(
            [job_vec], candidate_embeddings
        )[0]

        best_score = max(similarity_scores)

        if best_score >= min_similarity:
            matched.append(job_skill)
            total_score += best_score
        else:
            missing.append(job_skill)

    # ✅ Calculate percentage OUTSIDE loop
    max_score = len(job_skills)
    match_percentage = (total_score / max_score) * 100 if max_score > 0 else 0

    return {
        "matched": matched,
        "missing": missing,
        "match_count": len(matched),
        "total_required": len(job_skills),
        "match_percentage": round(match_percentage, 2)
    }