import os
import json
from typing import List, Dict
from .vectorestore import VectorStore

PROCESSED_JSONL = os.path.join(os.path.dirname(__file__), "data", "processed", "chunks.jsonl")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "data", "index")
EMBED_MODEL=os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

def load_chunks(path: str) -> List[Dict]:
    chunks: List[Dict] = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"Chunks file not found: {path} . Run ingest first.")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    if not chunks:
        raise RuntimeError(f"No chunks found in {path}. Run ingest first.")
    return chunks

def main():
    chunk=load_chunks(PROCESSED_JSONL)
    vs=VectorStore(embedding_model_name=EMBED_MODEL)
    vs.build(chunk)
    vs.save()
    print(f"Index built and saved to {vs.index_dir} with {len(vs.meta)} vectors.")

if __name__ == "__main__":
    main()