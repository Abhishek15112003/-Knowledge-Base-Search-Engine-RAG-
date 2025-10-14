from typing import List, Dict, Tuple
import math

def mmr_rerank(hits: List[Dict], top_n: int = 6, lambda_mult: float = 0.7) -> List[Dict]:
    if not hits:
        return []
    top_n = min(top_n, len(hits))

    # Normalize scores to [0,1]
    max_s = max(h.get("score", 0.0) for h in hits) or 1.0
    min_s = min(h.get("score", 0.0) for h in hits)
    rng = max_s - min_s if max_s != min_s else 1.0
    rel = [(h.get("score", 0.0) - min_s) / rng for h in hits]

    # Heuristic inter-item similarity via source+page equality (avoid near-duplicates)
    def sim(i: int, j: int) -> float:
        a, b = hits[i], hits[j]
        same_doc = 1.0 if a.get("source") == b.get("source") else 0.0
        same_page = 1.0 if a.get("page") == b.get("page") else 0.0
        # stronger penalty if same page (likely overlapping window)
        return 0.6 * same_doc + 0.4 * same_page

    selected: List[int] = []
    candidates = list(range(len(hits)))

    # pick the most relevant first
    best = max(range(len(hits)), key=lambda i: rel[i])
    selected.append(best)
    candidates.remove(best)

    while len(selected) < top_n and candidates:
        best_i = None
        best_score = -math.inf
        for i in candidates:
            diversity_penalty = 0.0
            for j in selected:
                diversity_penalty = max(diversity_penalty, sim(i, j))
            score = lambda_mult * rel[i] - (1 - lambda_mult) * diversity_penalty
            if score > best_score:
                best_score = score
                best_i = i
        selected.append(best_i)
        candidates.remove(best_i)

    return [hits[i] for i in selected]