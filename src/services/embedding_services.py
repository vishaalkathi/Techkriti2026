# src/services/embedding_service.py
from sentence_transformers import SentenceTransformer

# Load the model once globally
MODEL = SentenceTransformer("all-MiniLM-L6-v2")
def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Compute embeddings for a list of texts using the globally loaded model.
    """
    return MODEL.encode(texts, show_progress_bar=False)