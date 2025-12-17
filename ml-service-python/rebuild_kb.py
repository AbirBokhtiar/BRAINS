import os
import json
import numpy as np
import faiss
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Import your indexer utility
from app.indexer import build_index

load_dotenv()

# --- CONFIGURATION ---
# Ensure this matches the model used in main.py
EMBEDDING_MODEL_NAME = "models/text-embedding-004"
KB_FILE_PATH = Path("data/kb_texts.jsonl")

# Setup Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=api_key)

def get_gemini_embedding(text):
    """
    Generates embedding for a single text using Gemini.
    """
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL_NAME,
            contents=[text]
        )
        # Extract embedding values. 
        # structure: response.embeddings[0].values
        if response.embeddings:
            return response.embeddings[0].values
        return None
    except Exception as e:
        print(f"[ERROR] Failed to embed text: {text[:30]}... | {e}")
        return None

def main():
    if not KB_FILE_PATH.exists():
        print(f"❌ KB file not found at: {KB_FILE_PATH}")
        print("Please ensure you have a 'data/kb_texts.jsonl' file.")
        return

    print(f"📖 Reading documents from {KB_FILE_PATH}...")
    
    documents = []
    metadatas = []
    
    with open(KB_FILE_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            
            try:
                doc = json.loads(line)
                
                # Determine what text to embed. 
                # Adjust 'text', 'content', 'diagnosis' based on your JSONL structure.
                # Fallback to dumping the whole JSON if no specific text field exists.
                text_content = doc.get("text") or doc.get("content") or doc.get("summary") or json.dumps(doc)
                
                documents.append(text_content)
                metadatas.append(doc)
            except json.JSONDecodeError:
                print(f"[WARN] Skipping invalid JSON at line {i+1}")

    total_docs = len(documents)
    if total_docs == 0:
        print("❌ No documents found.")
        return

    print(f"🧠 Generating embeddings for {total_docs} documents using {EMBEDDING_MODEL_NAME}...")
    
    embeddings = []
    
    for i, doc_text in enumerate(documents):
        emb = get_gemini_embedding(doc_text)
        
        if emb is None:
            # Handle failure (skip or insert zero vector)
            # Here we skip to keep index clean
            print(f"[WARN] Skipping document {i} due to embedding failure.")
            # We must remove the corresponding metadata to keep lists aligned
            metadatas.pop(len(embeddings)) 
            continue
            
        embeddings.append(emb)
        
        if (i + 1) % 10 == 0:
            print(f"   Processed {i + 1}/{total_docs}...")

    if not embeddings:
        print("❌ No embeddings generated. Exiting.")
        return

    # Convert to NumPy array
    emb_array = np.array(embeddings, dtype="float32")
    
    # Optional: Normalize L2 (Generic advice: Gemini embeddings are often already normalized, 
    # but FAISS IndexFlatIP works best with normalized vectors for Cosine Similarity)
    faiss.normalize_L2(emb_array)

    dims = emb_array.shape[1]
    print(f"💾 Saving Index (Count: {len(emb_array)}, Dim: {dims})...")

    # Call the build_index function from your indexer.py
    build_index(emb_array, metadatas, dims)

    print("✅ Knowledge Base Rebuilt Successfully!")
    print(f"   - Index Dimensions: {dims}")
    print(f"   - Total Documents: {len(emb_array)}")

if __name__ == "__main__":
    main()