import re

from typing import List, Dict

WHITESPACE_RE = re.compile(r"\s+")
MULTI_NL_RE = re.compile(r"\n{3,}")

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("?", " ")
    text = WHITESPACE_RE.sub(" ", text)
    text = MULTI_NL_RE.sub("\n\n", text)
    return text.strip()

def chunk_text(text: str, max_tokens: int = 1000, overlap_tokens: int = 120) -> List[str]:
    words = text.split()
    if not words:
        return []
    chunks: List[str] = []
    start = 0
    step = max_tokens - overlap_tokens if max_tokens > overlap_tokens else max_tokens
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start += step
    return chunks

def build_chunk_records(source: str, page: int | None, text: str) -> List[Dict]:
    records: List[Dict] = []
    for idx, chunk in enumerate(chunk_text(text)):
        records.append({
            "source": source,
            "page": page,
            "chunk_id": idx,
            "content": chunk,
            "preview": chunk[:300]
        })

    return records
            