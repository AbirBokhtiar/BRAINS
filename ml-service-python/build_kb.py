# import os
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# # 1. Ensure directories exist
# if not os.path.exists("data"):
#     os.makedirs("data")

# # 2. Define your Knowledge Base (Sample Data)
# # If you already have a populated 'data/kb_texts.jsonl', you can skip defining this list 
# # and just read the file. But for safety, let's ensure consistent data.
# medical_texts = [
#     "Domain: Neurology. Subdomain: alzheimers. CaseID 101. Age 74. Symptoms: Memory loss, confusion. Diagnosis: Alzheimer's Disease.",
#     "Domain: Neurology. Subdomain: alzheimers. CaseID 102. Age 65. Symptoms: Difficulty speaking, motor issues. Diagnosis: Frontotemporal Dementia.",
#     "Domain: Cardiology. Subdomain: heart_failure. Symptoms: Shortness of breath, edema. Diagnosis: CHF.",
#     "Domain: Neurology. Subdomain: migraine. Symptoms: Headache, light sensitivity. Diagnosis: Migraine.",
#     "Domain: Neurology. Subdomain: alzheimers. Symptoms: progressive short-term memory loss, disorientation. Diagnosis: Early Stage Alzheimer's."
# ]

# # 3. Save text data to JSONL (so main.py can read the text later)
# print("Saving text data...")
# with open("data/kb_texts.jsonl", "w", encoding="utf-8") as f:
#     for text in medical_texts:
#         f.write(text + "\n")

# # 4. Load the SAME model used in main.py
# print("Loading model (all-MiniLM-L6-v2)...")
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# # 5. Create Embeddings
# print("Generating embeddings...")
# vectors = embedding_model.encode(medical_texts).astype("float32")

# # 6. Create FAISS Index
# d = vectors.shape[1]  # This will be 384 for MiniLM
# print(f"Vector dimension: {d}")

# index = faiss.IndexFlatL2(d)
# index.add(vectors)

# # 7. Save the Index
# faiss.write_index(index, "data/faiss.index")
# print("Success! FAISS index rebuilt.")

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Ensure directories exist
if not os.path.exists("data"):
    os.makedirs("data")

# 2. Define your Knowledge Base (Sample Data with metadata)
medical_texts = [
    {
        "id": 101,
        "domain": "neurology",
        "disease": "alzheimers",
        "age": 74,
        "symptoms": ["memory loss", "confusion"],
        "diagnosis": "Alzheimer's Disease",
        "text": "Domain: Neurology. Subdomain: alzheimers. CaseID 101. Age 74. Symptoms: Memory loss, confusion. Diagnosis: Alzheimer's Disease."
    },
    {
        "id": 102,
        "domain": "neurology",
        "disease": "frontotemporal_dementia",
        "age": 65,
        "symptoms": ["difficulty speaking", "motor issues"],
        "diagnosis": "Frontotemporal Dementia",
        "text": "Domain: Neurology. Subdomain: frontotemporal_dementia. CaseID 102. Age 65. Symptoms: Difficulty speaking, motor issues. Diagnosis: Frontotemporal Dementia."
    },
    {
        "id": 103,
        "domain": "cardiology",
        "disease": "heart_failure",
        "symptoms": ["shortness of breath", "edema"],
        "diagnosis": "CHF",
        "text": "Domain: Cardiology. Subdomain: heart_failure. Symptoms: Shortness of breath, edema. Diagnosis: CHF."
    },
    {
        "id": 104,
        "domain": "neurology",
        "disease": "migraine",
        "symptoms": ["headache", "light sensitivity"],
        "diagnosis": "Migraine",
        "text": "Domain: Neurology. Subdomain: migraine. Symptoms: Headache, light sensitivity. Diagnosis: Migraine."
    },
    {
        "id": 105,
        "domain": "neurology",
        "disease": "alzheimers",
        "symptoms": ["progressive short-term memory loss", "disorientation"],
        "diagnosis": "Early Stage Alzheimer's",
        "text": "Domain: Neurology. Subdomain: alzheimers. Symptoms: progressive short-term memory loss, disorientation. Diagnosis: Early Stage Alzheimer's."
    },
    {
        "id": 106,
        "domain": "pulmonology",
        "disease": "copd",
        "symptoms": ["persistent cough", "shortness of breath"],
        "diagnosis": "COPD",
        "text": "Domain: Pulmonology. Subdomain: copd. Symptoms: persistent cough, shortness of breath. Diagnosis: COPD."
    },
    {
        "id": 107,
        "domain": "cardiology",
        "disease": "heart_failure",
        "age": 68,
        "symptoms": ["fatigue", "swollen ankles"],
        "diagnosis": "Chronic Heart Failure",
        "text": "Domain: Cardiology. Subdomain: heart_failure. Age 68. Symptoms: fatigue, swollen ankles. Diagnosis: Chronic Heart Failure."
    }
]

# 3. Save text data to JSONL (JSON Lines format - one JSON object per line)
print("Saving text data as JSONL...")
with open("data/kb_texts.jsonl", "w", encoding="utf-8") as f:
    for doc in medical_texts:
        # Write each document as a JSON line (no newlines inside JSON)
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print(f"Saved {len(medical_texts)} documents to kb_texts.jsonl")

# 4. Extract text for embedding
texts_for_embedding = [doc["text"] for doc in medical_texts]

# 5. Load the SAME model used in main.py
print("Loading embedding model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 6. Create Embeddings
print("Generating embeddings...")
vectors = embedding_model.encode(texts_for_embedding).astype("float32")

# 7. Create FAISS Index
d = vectors.shape[1]  # This will be 384 for MiniLM
print(f"Vector dimension: {d}")

index = faiss.IndexFlatL2(d)
index.add(vectors)

# 8. Save the Index
faiss.write_index(index, "data/faiss.index")
print("✅ FAISS index built and saved to data/faiss.index")

# 9. Save metadata separately for reference
with open("data/kb_meta.json", "w", encoding="utf-8") as f:
    json.dump(medical_texts, f, ensure_ascii=False, indent=2)
print("✅ Metadata saved to data/kb_meta.json")

print("\n[SUCCESS] Knowledge Base Ready!")
print(f"- Documents: {len(medical_texts)}")
print(f"- Vector dimension: {d}")
print(f"- FAISS index size: {index.ntotal} vectors")