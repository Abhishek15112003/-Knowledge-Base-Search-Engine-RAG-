# backend/app.py
import os, io, uuid, re, difflib
from typing import Dict, List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ====== load env ======
load_dotenv()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ====== import your RAG pipeline for /query ======
# (Keep this if you want the multi-doc FAISS/Gemini path too)
try:
    from backend.rag_pipeline import query_pipeline  # Step 4 code
    HAVE_RAG_PIPELINE = True
    print("✓ RAG pipeline imported successfully")
except Exception as e:
    print(f"✗ Could not import RAG pipeline: {e}")
    HAVE_RAG_PIPELINE = False

print(f"HAVE_RAG_PIPELINE = {HAVE_RAG_PIPELINE}")

# ====== FastAPI app ======
app = FastAPI(title="Knowledge RAG API")

# CORS (open now; restrict origins for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # e.g., ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Health
# -------------------------------------------------
@app.get("/healthz")
def healthz():
    return {"ok": True, "message": "healthy"}

# -------------------------------------------------
# /query (multi-document RAG) — optional
# -------------------------------------------------
if HAVE_RAG_PIPELINE:
    class QueryIn(BaseModel):
        q: str
        k: Optional[int] = 8

    @app.post("/query")
    def query(inp: QueryIn):
        if not inp.q or not inp.q.strip():
            raise HTTPException(status_code=400, detail="q must be a non-empty string")
        return query_pipeline(inp.q, k=inp.k or 8)

# -------------------------------------------------
# Upload → Ask (single-file, per-session) — NEW
# -------------------------------------------------

# In-memory store: session_id -> {chunks, vectorizer, tfidf, meta}
SESSIONS: Dict[str, Dict] = {}

# ---- Helpers ----
def _clean_text(s: str) -> str:
    return " ".join((s or "").replace("\x00", " ").split())

# Query expansion for short queries
_SHORT_SYNONYMS = {
    "refund": ["refund", "refunds", "return", "returns", "refund policy", "money back", "5–7 business days", "5-7 business days", "30 days"],
    "return": ["return", "returns", "refund", "refund policy", "return window", "30 days"],
    "password": ["password", "reset password", "forgot password", "OTP", "one-time password"],
    "shipping": ["shipping", "delivery", "expedited", "standard shipping", "1–2 business days", "3–5 business days"],
    "support": ["support", "help", "customer support", "business hours", "9:00–18:00"],
    # add more domain synonyms as you like
}

def _normalize_query(q: str) -> str:
    q = (q or "").strip()
    q = re.sub(r"\s+", " ", q)
    return q

def _expand_query_if_short(q: str) -> str:
    """
    If the query is very short (<=2 tokens or <=12 chars), expand with synonyms.
    We concatenate terms so TF-IDF sees richer signal.
    """
    norm = _normalize_query(q)
    tokens = norm.lower().split()
    if len(tokens) <= 2 or len(norm) <= 12:
        # build a small synonym bag
        seeds = []
        for t in tokens:
            seeds += _SHORT_SYNONYMS.get(t, [t])
        # de-duplicate while preserving order
        seen, expanded = set(), []
        for w in seeds:
            if w not in seen:
                seen.add(w)
                expanded.append(w)
        # concatenate into a single query string
        return " ".join(expanded)
    return norm

def _contains_any(text: str, needles: List[str]) -> bool:
    t = text.lower()
    return any(n.lower() in t for n in needles if n)

def _closest_token(token: str, vocab_words: List[str]) -> str:
    # returns best match if similarity >= 0.8
    match = difflib.get_close_matches(token.lower(), vocab_words, n=1, cutoff=0.8)
    return match[0] if match else token.lower()

def _correct_short_query_tokens(q: str, vec) -> str:
    """
    For very short queries, correct each token to the nearest vocabulary term.
    """
    tokens = (q or "").lower().split()
    if not tokens:
        return q
    # build a small vocab list only once
    vocab_words = list(getattr(vec, "vocabulary_", {}).keys()) or []
    if not vocab_words:
        return q
    corrected = [_closest_token(t, vocab_words) for t in tokens]
    return " ".join(corrected)

def _extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for p in reader.pages:
        txt = p.extract_text() or ""
        pages.append(txt)
    return "\n\n".join(pages)

def _extract_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return file_bytes.decode("latin-1", errors="ignore")

def _chunk_text(text: str, max_words: int = 220, overlap: int = 40) -> List[str]:
    words = text.split()
    if not words:
        return []
    chunks, i = [], 0
    step = max_words - overlap if max_words > overlap else max_words
    while i < len(words):
        chunk = " ".join(words[i:i + max_words]).strip()
        if chunk:
            chunks.append(chunk)
        if i + max_words >= len(words):
            break
        i += step
    return chunks

def _build_index(chunks: List[str]):
    # Adjust parameters based on document size to avoid sklearn errors
    max_df = min(0.95, max(1, len(chunks) - 1)) if len(chunks) > 1 else 1.0
    min_df = 1 if len(chunks) > 5 else 1
    
    vec = TfidfVectorizer(
        stop_words="english",
        lowercase=True,
        strip_accents="unicode",
        sublinear_tf=True,
        max_df=max_df,
        min_df=min_df,
        ngram_range=(1, 2),  # <-- important for short queries
    )
    X = vec.fit_transform(chunks)
    return vec, X

def _retrieve(vec, X, chunks: List[str], query: str, top_k: int = 6) -> List[Dict]:
    original_q = _normalize_query(query)

    # correct typos for short queries using vectorizer vocabulary
    corrected_q = _correct_short_query_tokens(original_q, vec)

    # expand short queries with synonyms (you already added _expand_query_if_short)
    expanded_q = _expand_query_if_short(corrected_q)

    # cosine over expanded query
    qv = vec.transform([expanded_q])
    sims = cosine_similarity(qv, X).ravel()

    # light lexical boost if very short and exact word appears
    tokens = corrected_q.split()
    is_short = (len(tokens) <= 2 or len(corrected_q) <= 12)
    if is_short and tokens:
        for i, c in enumerate(chunks):
            text_low = c.lower()
            if any(t in text_low for t in tokens):
                sims[i] += 0.15  # small bump for exact containment

    idxs = sims.argsort()[::-1][:top_k]
    out = []
    for rank, i in enumerate(idxs, start=1):
        out.append({
            "rank": rank,
            "score": float(sims[i]),
            "content": chunks[i]
        })
    return out

def _build_context(hits: List[Dict], *, max_blocks: int = 4, budget_chars: int = 1600) -> str:
    """
    Build a compact, clearly delimited context so the model can't 'see' everything.
    """
    buf, used, count = [], 0, 0
    for i, h in enumerate(hits, start=1):
        if count >= max_blocks: 
            break
        text = (h.get("content") or h.get("text") or "").strip()
        if not text: 
            continue
        block = f"[{i}] BEGIN\n{text}\nEND\n"
        if used + len(block) > budget_chars:
            # if last block doesn't fit, try a truncated slice
            remain = max(0, budget_chars - used - len(f"[{i}] BEGIN\n") - len("\nEND\n"))
            snippet = (text[:remain]).rstrip()
            if snippet:
                buf.append(f"[{i}] BEGIN\n{snippet}\nEND\n")
            break
        buf.append(block)
        used += len(block)
        count += 1
    return "\n".join(buf)

def _gemini_answer(question: str, context: str, *, strict: bool = True) -> str:
    """
    Strictly grounded answerer:
    - Uses ONLY provided context.
    - 1–4 sentences max.
    - Requires bracket citations [1], [2] matching CONTEXT blocks.
    - Falls back to 'I don't know based on the provided document.' if not grounded.
    """
    import re

    def _fallback():
        # Short, safe extractive fallback (not the whole doc)
        lines = [l for l in context.splitlines() if l and not l.startswith("[") and l not in ("BEGIN", "END")]
        snippet = " ".join(lines)[:400]
        return snippet or "I don't know based on the provided document."

    if not context.strip():
        return "I don't know based on the provided document."

    # If no key configured, don't dump the whole text — return short extract
    if not GOOGLE_API_KEY:
        return _fallback()

    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)

        system = (
            "You answer ONLY using the numbered CONTEXT blocks.\n"
            "If the answer is not fully supported by CONTEXT, reply exactly:\n"
            "\"I don't know based on the provided document.\"\n"
            "Every factual sentence MUST include a bracket citation like [1] or [2]."
        )

        rules = (
            "Rules:\n"
            "1) Use only the provided CONTEXT.\n"
            "2) 1–4 short sentences. Be concise.\n"
            "3) Every sentence MUST include a citation [n].\n"
            "4) If unsupported, say: I don't know based on the provided document."
        )

        prompt = (
            f"{system}\n\n{rules}\n\n"
            f"QUESTION:\n{question}\n\n"
            f"CONTEXT (numbered blocks):\n{context}\n\n"
            "Answer:"
        )

        generation_config = {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 160,   # keep it tight
        }

        model = genai.GenerativeModel(GEMINI_MODEL, generation_config=generation_config)
        raw = (model.generate_content(prompt).text or "").strip()

        if not raw:
            return "I don't know based on the provided document."

        if strict:
            # Require at least one [n] citation
            has_citation = re.search(r"\[\d+\]", raw) is not None

            # Limit to 4 sentences max (split on . ! ?)
            sentences = re.split(r"(?<=[.!?])\s+", raw.strip())
            sentences = [s for s in sentences if s]
            if len(sentences) > 4:
                sentences = sentences[:4]
            trimmed = " ".join(sentences)

            # Require citations on each sentence
            all_cited = all(re.search(r"\[\d+\]", s) for s in sentences)

            # Simple overlap check: ensure significant token overlap with context
            ctx_text = " ".join([l for l in context.splitlines() if not l.startswith("[")])
            ctx_tokens = set(re.findall(r"[A-Za-z0-9]+", ctx_text.lower()))
            ans_tokens = re.findall(r"[A-Za-z0-9]+", trimmed.lower())
            overlap = sum(1 for t in ans_tokens if t in ctx_tokens)
            grounded_ratio = overlap / max(len(ans_tokens), 1)

            if not has_citation or not all_cited or grounded_ratio < 0.3:
                return "I don't know based on the provided document."

            return trimmed

        return raw

    except Exception as e:
        # If Gemini errors, don't dump everything — return short extract
        return _fallback()

# ---- Schemas for /ask ----
class AskIn(BaseModel):
    session_id: str
    q: str
    k: Optional[int] = 6
    strict: Optional[bool] = True  # default ON

# ---- Routes ----
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    Accept a single PDF or TXT, extract & chunk text,
    build a TF-IDF index for this session, and return session_id.
    """
    fname = (file.filename or "").lower()
    data = await file.read()

    if fname.endswith(".pdf"):
        raw = _extract_pdf(data)
    elif fname.endswith(".txt"):
        raw = _extract_txt(data)
    else:
        raise HTTPException(status_code=400, detail="Only .pdf and .txt are supported.")

    text = _clean_text(raw)
    if not text:
        raise HTTPException(status_code=422, detail="No readable text found (maybe scanned PDF?).")

    chunks = _chunk_text(text, max_words=220, overlap=40)
    if not chunks:
        raise HTTPException(status_code=422, detail="Could not create chunks from the file.")

    vec, X = _build_index(chunks)
    sid = str(uuid.uuid4())
    SESSIONS[sid] = {"chunks": chunks, "vectorizer": vec, "tfidf": X, "meta": {"filename": file.filename}}
    return {"session_id": sid, "chunks": len(chunks), "filename": file.filename}

@app.post("/ask")
def ask(inp: AskIn):
    s = SESSIONS.get(inp.session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Invalid or expired session_id. Upload again.")
    k = int(inp.k or 6)

    # Tighter retrieval improves grounding
    k = min(k, 4)

    hits = _retrieve(s["vectorizer"], s["tfidf"], s["chunks"], inp.q, top_k=k)
    context = _build_context(hits, max_blocks=min(4, k), budget_chars=1600)
    answer = _gemini_answer(inp.q, context, strict=True)

    citations = [{"id": i + 1, "source": s["meta"]["filename"]} for i, _ in enumerate(hits)]
    return {"answer": answer, "citations": citations, "retrieved": hits, "filename": s["meta"]["filename"]}

@app.get("/debug/models")
def debug_models():
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        models = [m.name for m in genai.list_models()]
        return {"models": models}
    except Exception as e:
        return {"error": str(e)}
