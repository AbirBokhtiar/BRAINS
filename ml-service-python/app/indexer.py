# ml-service-python/app/indexer.py
import json
from pathlib import Path
import numpy as np
import faiss

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "kb_texts.jsonl"
INDEX_PATH = Path(__file__).resolve().parent.parent / "data" / "faiss.index"
META_PATH = Path(__file__).resolve().parent.parent / "data" / "kb_meta.json"

_index = None
_meta = None
_dim = None

def build_index(embeddings: np.ndarray, meta: list, dim: int):
    """
    embeddings: numpy array (n, dim) normalized (for IP ~ cosine if normalized)
    meta: list[dict] with same order as embeddings
    """
    global _index, _meta, _dim
    _dim = dim
    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype('float32')
    # Use inner product index (assumes normalized embeddings for cosine similarity)
    idx = faiss.IndexFlatIP(dim)
    idx.add(embeddings)
    faiss.write_index(idx, str(INDEX_PATH))
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    _index = idx
    _meta = meta

def load_index():
    global _index, _meta, _dim
    if not INDEX_PATH.exists() or not META_PATH.exists():
        return False
    idx = faiss.read_index(str(INDEX_PATH))
    _index = idx
    with open(META_PATH, "r", encoding="utf-8") as f:
        _meta = json.load(f)
    # IndexFlat has attribute d
    try:
        _dim = int(idx.d)
    except Exception:
        _dim = None
    return True

def search(query_emb, top_k=5):
    """
    query_emb: 1d numpy array (dim,) or 2d (1,dim)
    returns list of {score, **meta}
    """
    global _index, _meta
    if _index is None:
        loaded = load_index()
        if not loaded:
            raise RuntimeError("Index not built or available")
    q = np.asarray(query_emb, dtype='float32')
    if q.ndim == 1:
        q = q.reshape(1, -1)
    scores, indices = _index.search(q, top_k)
    results = []
    for idx, score in zip(indices[0], scores[0]):
        if idx < 0 or idx >= len(_meta):
            continue
        item = {"score": float(score)}
        # merge meta fields (avoid overwriting score)
        meta_item = _meta[idx].copy()
        item.update(meta_item)
        results.append(item)
    return results