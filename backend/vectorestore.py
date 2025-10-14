import os
import json
import faiss
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2", index_dir: str = None, normalize: bool = True):
        if index_dir is None:
            index_dir = os.path.join(os.path.dirname(__file__), "data", "index")
        self.index_dir = index_dir
        self.model_name = embedding_model_name
        self.normalize = normalize
        self.model = SentenceTransformer(embedding_model_name)
        self.index = None
        self.meta: List[Dict] = []
        self.dim = self.model.get_sentence_embedding_dimension()
    @property
    def index_path(self):
        return os.path.join(self.index_dir, "faiss.index")
    @property
    def meta_path(self):
        return os.path.join(self.index_dir, "meta.jsonl")
    
    @property
    def stats_path(self):
        return os.path.join(self.index_dir, "stats.json")
    
    def ensure_index_dir(self):
        os.makedirs(self.index_dir, exist_ok=True)
    
    def encode(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        if self.normalize:
            faiss.normalize_L2(embeddings)
        return embeddings
    
    def build(self,chunks: List[Dict]):
        self.ensure_index_dir()
        texts = [c["content"] for c in chunks]
        self.meta = chunks
        embeddings = self.encode(texts)
        self.index = faiss.IndexFlatIP(self.dim) 
        self.index.add(embeddings)
        self.meta = chunks

    def save(self):
        self.ensure_index_dir()
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            for m in self.meta:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")
        
        with open(self.stats_path, "w", encoding="utf-8") as f:
            json.dump({
                "model": self.model_name,
                "normalize": self.normalize,
                "dim": self.dim,
                "count": len(self.meta)
            }, f, ensure_ascii=False, indent=2)
    
    def load(self):
        self.index = faiss.read_index(self.index_path)
        self.meta = []
        with open(self.meta_path, "r", encoding="utf-8") as f:
            for line in f:
                self.meta.append(json.loads(line))
    
    def search(self, query: str, top_k: int = 8) -> List[Dict]:
        q=self.encode([query])
        scores,idxs=self.index.search(q, top_k)
        out: List[Dict] = []

        for score, idx in zip(scores[0], idxs[0]):
            if idx<0 or idx>=len(self.meta):
                continue
            item = self.meta[idx].copy()
            item["score"] = float(score)
            out.append(item)
        return out