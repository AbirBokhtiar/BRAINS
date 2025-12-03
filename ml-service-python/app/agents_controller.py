# # ml-service-python/app/agents.py
# import os, json
# from .encoder import encode
# from .indexer import build_index, load_index, search
# from pathlib import Path

# KB_FILE = Path(__file__).resolve().parent.parent / "data" / "kb_texts.jsonl"

# # Simple LLM stub function — replace this with real provider call (OpenAI/Gemini).
# def llm_call_stub(prompt: str) -> str:
#     # This is a deterministic, safe placeholder summarizer.
#     # For real usage, swap with openai.ChatCompletion or Gemini API.
#     # Keep it conservative: provide short classification using heuristics.
#     # If "MMSE" appears, try to infer coarse label:
#     if "MMSE:" in prompt:
#         try:
#             idx = prompt.index("MMSE:")
#             mmse_val = int(prompt[idx: idx+12].split()[1].strip().strip(","))
#             if mmse_val >= 27:
#                 diag = "Normal cognition"
#             elif mmse_val >= 24:
#                 diag = "Very Mild Alzheimer's Disease"
#             elif mmse_val >= 20:
#                 diag = "Mild Alzheimer's Disease"
#             elif mmse_val >= 14:
#                 diag = "Moderate Alzheimer's Disease"
#             else:
#                 diag = "Severe Alzheimer's Disease"
#             rationale = f"Rule-based heuristic: MMSE {mmse_val} suggests '{diag}'. Use clinical confirmation."
#             return f"{diag}\n\nRationale: {rationale}"
#         except Exception:
#             pass
#     return "Uncertain\n\nRationale: insufficient data for rule-based diagnosis. Replace with LLM call."

# def format_patient_text(patient) -> str:
#     fields = []
#     for k,v in patient.items():
#         if v is None or v == "":
#             continue
#         fields.append(f"{k.capitalize()}: {v}")
#     return ", ".join(fields)

# def build_kb_index(force_rebuild=False):
#     """
#     Read KB file, encode texts, build a persistent FAISS index + meta file
#     """
#     # load KB lines
#     with open(KB_FILE, "r", encoding="utf8") as f:
#         items = [json.loads(l) for l in f]
#     texts = [it["text"] for it in items]
#     embeddings = encode(texts)
#     import numpy as np
#     meta = items  # list of dicts with case_id and text
#     build_index(np.array(embeddings), meta, embeddings.shape[1])
#     return len(items)

# def retrieve_for_patient_text(text, k=5):
#     # encode query
#     emb = encode([text])[0]
#     results = search(emb, top_k=k)
#     return results[0]

# def diagnose_patient(patient: dict, k=5):
#     T = format_patient_text(patient)
#     retrieved = retrieve_for_patient_text(T, k=k)
#     # Build prompt for LLM (fused)
#     prompt_parts = []
#     prompt_parts.append("You are a professional neurologist specializing in Alzheimer's disease diagnosis.")
#     prompt_parts.append("Provide a short diagnosis (single line) and a clinical rationale.")
#     prompt_parts.append("Target patient (T):")
#     prompt_parts.append(T)
#     prompt_parts.append("\nRetrieved similar cases (R):")
#     for i, r in enumerate(retrieved, start=1):
#         prompt_parts.append(f"Case {i}: {r['text']} (score: {r['score']:.4f})")
#     prompt = "\n".join(prompt_parts)
#     llm_out = llm_call_stub(prompt)
#     # parse LLM stub output: diag + rationale
#     parts = llm_out.split("\n\n", 1)
#     diagnosis = parts[0].strip()
#     rationale = parts[1].replace("Rationale:", "").strip() if len(parts) > 1 else ""
#     return {"diagnosis": diagnosis, "rationale": rationale, "retrieved": retrieved, "prompt": prompt}

######################

# ml-service-python\app\agents_controller.py
# import json
# from pathlib import Path
# from typing import List, Dict
# import numpy as np

# from .encoder import encode
# from .indexer import build_index, load_index, search
# from .ml_core import prompt_builder, llm_connector

# KB_FILE = Path(__file__).resolve().parent.parent / "data" / "kb_texts.jsonl"

# def llm_call_stub(prompt: str) -> str:
#     # delegate to ml_core llm connector (keeps backward compatible stub)
#     return llm_connector.generate(prompt)

# def format_patient_text(patient: Dict) -> str:
#     parts = []
#     for k, v in patient.items():
#         if v is None:
#             continue
#         parts.append(f"{k}: {v}")
#     return " | ".join(parts)

# def build_kb_index(force_rebuild: bool = False):
#     """
#     Build FAISS index from data/kb_texts.jsonl
#     Each line in kb_texts.jsonl is expected to be a JSON object with 'text' and optional metadata.
#     """
#     # if index already exists and not forcing rebuild, try to load
#     if not force_rebuild:
#         try:
#             ok = load_index()
#             if ok:
#                 return True
#         except Exception:
#             pass

#     if not KB_FILE.exists():
#         raise FileNotFoundError(f"KB file not found: {KB_FILE}")

#     docs = []
#     texts = []
#     with open(KB_FILE, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue
#             try:
#                 obj = json.loads(line)
#             except Exception:
#                 continue
#             # ensure minimal fields
#             docs.append(obj)
#             texts.append(obj.get("text", "")[:10000])

#     if len(texts) == 0:
#         raise RuntimeError("No KB documents to index")

#     embs = encode(texts, batch_size=32)
#     # SentenceTransformer returns numpy array shape (n, dim)
#     if isinstance(embs, list):
#         embs = np.array(embs, dtype='float32')
#     elif isinstance(embs, np.ndarray) and embs.dtype != np.float32:
#         embs = embs.astype('float32')

#     dim = int(embs.shape[1])
#     build_index(embs, docs, dim)
#     return True

# def retrieve_for_patient_text(text: str, k: int = 5):
#     # create embedding for query text
#     q_emb = encode([text], batch_size=1)
#     if isinstance(q_emb, np.ndarray):
#         q_emb = q_emb[0]
#     return search(q_emb, top_k=k)

# def diagnose_patient(patient: Dict, k: int = 5) -> Dict:
#     query = format_patient_text(patient)
#     retrieved = retrieve_for_patient_text(query, k=k)
#     # build prompt
#     prompt = prompt_builder.build_prompt(patient, retrieved, disease=patient.get("disease","unspecified"))
#     llm_out = llm_call_stub(prompt)
#     # return structured object
#     return {
#         "diagnosis": llm_out.splitlines()[0] if llm_out else "No diagnosis",
#         "rationale": llm_out,
#         "retrieved": retrieved
#     }