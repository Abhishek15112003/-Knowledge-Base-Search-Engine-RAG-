import os
import json
from typing import List, Dict
from pypdf import PdfReader
from .chunking import clean_text, build_chunk_records

# Try to import chardet; fall back gracefully
try:
    from chardet.universaldetector import UniversalDetector
except Exception:
    UniversalDetector = None  # we'll handle this below

RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
OUTPUT_JSONL = os.path.join(PROCESSED_DIR, "chunks.jsonl")

def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def read_pdf(path: str) -> List[Dict]:
    reader = PdfReader(path)
    out: List[Dict] = []
    for i, page in enumerate(reader.pages):
        raw = page.extract_text() or ""
        txt = clean_text(raw)
        if txt:
            out.extend(build_chunk_records(os.path.basename(path), i + 1, txt))
    return out

def detect_encoding(path: str) -> str:
    if UniversalDetector is None:
        return "utf-8"
    detector = UniversalDetector()
    with open(path, "rb") as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result.get("encoding") or "utf-8"

def read_txt(path: str) -> List[Dict]:
    try:
        enc = detect_encoding(path)
        with open(path, "r", encoding=enc, errors="ignore") as f:
            raw = f.read()
    except Exception:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    txt = clean_text(raw)
    if not txt:
        return []
    return build_chunk_records(os.path.basename(path), None, txt)

def walk_and_ingest(raw_dir: str) -> List[Dict]:
    records: List[Dict] = []
    for root, _, files in os.walk(raw_dir):
        for fn in files:
            path = os.path.join(root, fn)
            lower = fn.lower()
            if lower.endswith(".pdf"):
                records.extend(read_pdf(path))
            elif lower.endswith((".txt", ".md")):
                records.extend(read_txt(path))
            else:
                continue
    return records

def write_jsonl(path: str, records: List[Dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    ensure_dirs()
    records = walk_and_ingest(RAW_DIR)
    if not records:
        print("[ingest] No usable text found in data/raw. Add PDFs/TXT and rerun.")
        return
    write_jsonl(OUTPUT_JSONL, records)
    print(f"[ingest] Wrote {len(records)} chunk records → {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
