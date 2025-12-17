import os
import json
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from pathlib import Path
from contextlib import asynccontextmanager
from openai import OpenAI
import traceback

from .schemas import PatientInput, RetrieveRequest
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Import orchestrator and agents
from .agents.orchestrator.orchestrator import orchestrate
from . import encoder as enc_module

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
faiss_index_path = "data/faiss.index"
if not Path(faiss_index_path).exists():
    raise RuntimeError("FAISS index not found. Run KB builder.")

index = faiss.read_index(faiss_index_path)

# Load documents aligned with FAISS vectors
with open("data/kb_texts.jsonl", "r", encoding="utf-8") as f:
    documents = [json.loads(line.strip()) if line.strip() else {} for line in f.readlines()]

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def retrieve_documents(query: str, k: int = 5):
    """Retrieve documents from FAISS index."""

    # Generate embedding
    q_emb = embedding_model.encode([query]).astype("float32")

    # Search FAISS
    scores, indices = index.search(q_emb, k)
    
    # Validate indices to prevent crashes if index is out of sync
    valid_indices = [i for i in indices[0] if i < len(documents)]
    if not valid_indices:
        print("[WARN] No valid documents found in index.")
        return []
    
    # Retrieve documents
    retrieved_docs = [documents[i] for i in valid_indices]
    return retrieved_docs


def rag_query_with_orchestrator(patient_data: dict, k: int = 5):
    """
    Use the orchestrator to route to the correct domain and disease agent.
    Each agent performs RAG + LLM inference.
    """
    try:
        # Step 1: Orchestrate (determine domain and disease agent)
        orchestration_result = orchestrate(patient_data)
        
        print(f"[DEBUG] Orchestration result: {json.dumps(orchestration_result, indent=2, default=str)}")
        
        domain = orchestration_result.get("domain", "general")
        agent_name = orchestration_result.get("agent", "general_medical_assistant")
        
        print(f"[INFO] Orchestrator routed to domain='{domain}', agent='{agent_name}'")
        
        # Step 2: Get diagnosis from agent
        # (Agent internally does RAG + LLM call)
        diagnosis_result = orchestration_result.get("diagnosis", {})
        
        print(f"[DEBUG] Diagnosis result from agent: {json.dumps(diagnosis_result, indent=2, default=str)}")
        
        return {
            "domain": domain,
            "agent": agent_name,
            "diagnosis": diagnosis_result.get("summary", "No diagnosis"),
            "rationale": diagnosis_result.get("rationale", ""),
            "retrieved": diagnosis_result.get("evidence", []),
            "scores": diagnosis_result.get("scores", []),
            "confidence": diagnosis_result.get("confidence", 0)
        }
    
    except Exception as e:
        print(f"[ERROR] Orchestration failed: {str(e)}")
        traceback.print_exc()
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] ML Service Ready. FAISS + Multi-Agent System Loaded.")
    yield


app = FastAPI(title="BRAINS ML Service (Multi-Agent)", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ml-service-python-multi-agent"}


@app.post("/api/retrieve")
async def retrieve(request: Request):
    """Robust retrieve endpoint: accept JSON body {text, k} or plain/raw text payloads.
    This avoids 422 errors when clients send non-standard bodies.
    """
    try:
        content_type = request.headers.get("content-type", "")
        text = ""
        k = 5

        # Try JSON first for application/json
        if "application/json" in content_type:
            body = await request.json()
            if isinstance(body, dict):
                text = body.get("text") or body.get("query") or ""
                k = int(body.get("k", 5) or 5)
            else:
                # body might be a raw value (e.g. a string)
                text = str(body)

        else:
            # Not JSON: accept raw bytes or fallback to reading body and attempting JSON parse
            raw = await request.body()
            raw_text = raw.decode("utf-8").strip()
            if not raw_text:
                # If nothing provided, return empty docs
                return {"docs": []}

            # Attempt to parse raw as JSON object
            try:
                parsed = json.loads(raw_text)
                if isinstance(parsed, dict):
                    text = parsed.get("text") or parsed.get("query") or ""
                    k = int(parsed.get("k", 5) or 5)
                else:
                    text = str(parsed)
            except Exception:
                # Treat the raw text as the query string itself
                text = raw_text

        if not text:
            raise HTTPException(status_code=400, detail="Empty retrieve query; provide 'text' in JSON or raw body.")

        print(f"\n[DEBUG] Processing Retrieve Request: {text[:50]}... (k={k})")

        # Use helper to get documents
        results = retrieve_documents(text, k)

        print(f"[DEBUG] Found {len(results)} documents.")
        return {"docs": results}

    except HTTPException:
        raise
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("RETRIEVE CRASH DETECTED:")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/api/ml/diagnose")
# async def diagnose(patient: PatientInput):
#     """
#     Multi-agent diagnosis endpoint.
#     Routes patient to appropriate domain → disease agent.
#     Each agent performs RAG + LLM inference.
#     """
#     try:
#         patient_dict = patient.dict()
#         print(f"\n[DEBUG] Patient Input: {patient_dict}")
        
#         # Convert symptoms to list if string (handle both formats)
#         if isinstance(patient_dict.get('symptoms'), str):
#             symptoms_list = [s.strip() for s in patient_dict['symptoms'].split(',') if s.strip()]
#         elif isinstance(patient_dict.get('symptoms'), list):
#             symptoms_list = patient_dict['symptoms']
#         else:
#             symptoms_list = []
        
#         # Update dict with normalized symptoms list
#         patient_dict['symptoms'] = symptoms_list
        
#         # Use orchestrator to route and diagnose
#         result = rag_query_with_orchestrator(patient_dict, k=3)
        
#         print(f"\n[DEBUG] Diagnosis Result: {result}")
        
#         return {
#             "domain": result.get("domain"),
#             "agent": result.get("agent"),
#             "diagnosis": result.get("diagnosis"),
#             "rationale": result.get("rationale"),
#             "retrieved": result.get("retrieved", []),
#             "scores": result.get("scores", []),
#             "confidence": result.get("confidence", 0)
#         }
    
#     except Exception as e:
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         print("DIAGNOSE CRASH DETECTED:")
#         traceback.print_exc()
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ml/diagnose/{domain}")
async def diagnose_with_domain(domain: str, patient: PatientInput):
    """
    Diagnose with explicit domain override.
    Useful for testing specific domains.
    """
    try:
        patient_dict = patient.dict()
        patient_dict["_requested_domain"] = domain  # Pass domain hint
        
        print(f"\n[DEBUG] Diagnose for domain '{domain}': {patient_dict}")

        # # Convert symptoms to list if string (handle both formats)
        # if isinstance(patient_dict.get('symptoms'), str):
        #     symptoms_list = [s.strip() for s in patient_dict['symptoms'].split(',') if s.strip()]
        # elif isinstance(patient_dict.get('symptoms'), list):
        #     symptoms_list = patient_dict['symptoms']
        # else:
        #     symptoms_list = []
        
        # # Update dict with normalized symptoms list
        # patient_dict['symptoms'] = symptoms_list
        
        result = rag_query_with_orchestrator(patient_dict, k=3)
        
        return {
            "domain": result.get("domain"),
            "agent": result.get("agent"),
            "diagnosis": result.get("diagnosis"),
            "confidence": result.get("confidence"),
            "scores": result.get("scores", []),
            "rationale": result.get("rationale"),
            "retrieved": result.get("retrieved", [])
        }
    
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("DIAGNOSE WITH DOMAIN CRASH DETECTED:")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
