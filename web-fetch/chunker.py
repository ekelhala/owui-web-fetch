from .constants import CHUNK_SIZE, OVERLAP

def chunk_text(text: str) -> list[str]:
    """
    Split the cleaned text into overlapping chunks.
    """
    return [
        text[i : i + CHUNK_SIZE]
        for i in range(0, len(text), CHUNK_SIZE - OVERLAP)
    ]