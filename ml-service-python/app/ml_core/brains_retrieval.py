# ml-service-python\app\ml_core\brains_retrieval.py
from typing import List, Dict
from .. import encoder as _enc  # relative import if used as package
from .. import indexer as _idx
import numpy as np

def retrieve(query: str, k: int = 3) -> List[Dict]:
    """
    Backwards-compatible retrieval wrapper that uses FAISS index via indexer.
    """
    q_emb = _enc.encode([query], batch_size=1)
    if isinstance(q_emb, np.ndarray):
        q_emb = q_emb[0]
    return _idx.search(q_emb, top_k=k)