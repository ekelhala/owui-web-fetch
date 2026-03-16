from .constants import CHUNK_SIZE, OVERLAP

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """
    Split the cleaned text into overlapping chunks.
    """
    return [
        text[i : i + chunk_size]
        for i in range(0, len(text), chunk_size - overlap)
    ]