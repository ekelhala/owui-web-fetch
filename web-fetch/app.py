from fastapi import FastAPI
from pydantic import BaseModel
import json

from .constants import CHUNK_SIZE
from .fetcher import fetch_page
from .cleaner import clean_text
from .chunker import chunk_text
from .semantic import rank_chunks

app = FastAPI()

class SearchRequest(BaseModel):
    urls: str | list[str]
    search_query: str
    top_k: int = 3

@app.post("/semantic-search")
def semantic_search(req: SearchRequest) -> str:
    """
    FastAPI endpoint that receives the request, runs the semantic search
    pipeline and returns a Markdown string with the best matches.
    """
    urls = [req.urls] if isinstance(req.urls, str) else req.urls
    preview = ""

    all_chunks = []
    errors = []

    for url in urls:
        try:
            html = fetch_page(url)
            txt = clean_text(html)
            if not preview:
                preview = txt[:1500]
            all_chunks.extend([(url, ch) for ch in chunk_text(txt)])
        except Exception as exc:
            errors.append(f"error: **{url}** - {exc}")

    if not all_chunks:
        if errors:
            return "\n\n".join(errors)
        return "No text content could be extracted from the provided URLs."

    chunk_texts = [c for _, c in all_chunks]
    ranked = rank_chunks(chunk_texts, req.search_query, req.top_k)

    md_chunks = []
    for idx, txt, score in ranked:
        src, _ = all_chunks[idx]
        md_chunks.append(
            f"### Match from `{src}`\n"
            f"*Score:* {score:.2f}\n\n"
            f"{txt}\n"
        )

    if not md_chunks:
        if errors:
            return "\n\n".join(errors)
        return (
            f"No highly relevant matches found for '{req.search_query}'.\n"
            f"Content preview:\n{preview}"
        )

    if errors:
        md_chunks.append("\n---\n\n".join(errors))

    return "\n---\n\n".join(md_chunks)