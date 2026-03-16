from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .constants import MIN_SCORE

model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_chunks(
    chunks: List[str],
    query: str,
    top_k: int,
    min_score: float = MIN_SCORE,
) -> List[tuple[int, str, float]]:
    """
    Return a list of (chunk_index, chunk_text, similarity_score) sorted
    from highest to lowest.  Only chunks with similarity >= min_score are kept.
    """
    chunk_embeddings = model.encode(chunks)
    query_emb = model.encode([query])
    similarities = cosine_similarity(query_emb, chunk_embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = []
    for idx in top_indices:
        score = similarities[idx]
        if score < min_score:
            continue
        results.append((idx, chunks[idx], score))
    return results