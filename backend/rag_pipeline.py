import os,json
from typing import List, Dict
from backend.rerank import mmr_rerank

INDEX_DIR = os.path.join(os.path.dirname(__file__), "data", "index")
STATS_PATH = os.path.join(INDEX_DIR, "stats.json")

def load_provider_from_stats()-> str:
    if os.path.exists(STATS_PATH):
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            stats = json.load(f)
            return stats.get("provider", "sbert")
    return "sbert"

def get_vectorstore():
    provider=load_provider_from_stats()
    if provider=="openai":
        from .vectorstore_openai import VectorStoreOpenAI as VS
        return VS(INDEX_DIR)
    elif provider=="fastembed":
        from .vectorstore_pinecone import VectorStoreFastEmbed as VS
        return VS(INDEX_DIR)
    else:
        from .vectorestore import VectorStore as VS
        return VS(index_dir=INDEX_DIR)
    
SYSTEM_PROMPT=("You are a helpful assistant. Answer ONLY using the provided context. "
"If the answer is not present, say you don't know. Keep it concise. "
"Cite sources in square brackets like [1], [2].")


def build_context(chunks:List[Dict],budget_chars:int =5000)->str:
    buf, used = [], 0
    for i,c in enumerate(chunks,start=1):
        snippet=c.get("content")or c.get("text")or ""
        header=f"[{i}] Source: {c.get('source')} page {c.get('page')}\n"
        if used+len(snippet)+len(header)>budget_chars:
            break
        buf.append(header+snippet+"\n\n")

        used+=len(snippet)+len(header)
    return "".join(buf).strip()

class Answerer:

    def __init__(self):
        self.api_key=os.getenv("Google_API_KEY")
        self.model_name=os.getenv("GOOGLE_MODEL","gemini-1.5-flash")
        self.model=None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model=genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Error initializing Google Generative AI: {e}")
                self.model=None
   
    def answer(self, question: str, context: str) -> str:
        if not context.strip():
            return "I don't know based on the provided documents."
        if self.model is None:
# simple extractive fallback
            lines = [l for l in context.splitlines() if l and not l.startswith("[")]
            summary = " ".join(lines)[:900]
            return summary + (" [1]" if summary else "")
        try:
            prompt = (
                f"{SYSTEM_PROMPT}\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"Question: {question}\nAnswer:")
            resp = self.model.generate_content(prompt)
            return (resp.text or "").strip() or "I don't know."
        except Exception:
            lines = [l for l in context.splitlines() if l and not l.startswith("[")]
            summary = " ".join(lines)[:900]
            return summary + (" [1]" if summary else "")




def query_pipeline(q: str, k: int = 8) -> Dict:
    vs = get_vectorstore()
    vs.load()
    hits = vs.search(q, top_k=k)
    # apply MMR reranking on the retrieved hits
    reranked = mmr_rerank(hits, top_n=min(6, k), lambda_mult=0.7)
    context = build_context(reranked)
    ans = Answerer().answer(q, context)
    citations = [{"id": i + 1, "source": h.get("source"), "page": h.get("page")}
        for i, h in enumerate(reranked)]
    return {"answer": ans, "citations": citations, "retrieved": reranked}