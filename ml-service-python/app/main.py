
# # ml-service-python/app/main.py
# import os
# import json
# from dotenv import load_dotenv
# load_dotenv()

# from fastapi import FastAPI, HTTPException
# from pathlib import Path
# from contextlib import asynccontextmanager
# from openai import OpenAI

# import traceback
# from .schemas import RetrieveRequest
# from .agents import retrieve_for_patient_text

# from .schemas import PatientInput
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np

# # -----------------------------
# # Load embedding model
# # -----------------------------
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# # -----------------------------
# # Load FAISS index
# # -----------------------------
# faiss_index_path = "data/faiss.index"
# if not Path(faiss_index_path).exists():
#     raise RuntimeError("FAISS index not found. Run KB builder.")

# index = faiss.read_index(faiss_index_path)

# # Load documents aligned with FAISS vectors
# with open("data/kb_texts.jsonl", "r", encoding="utf-8") as f:
#     documents = [line.strip() for line in f.readlines()]

# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# # # Core RAG process
# # def rag_query(domain: str, query: str, k=3):
# #     q_emb = embedding_model.encode([query]).astype("float32")
# #     scores, indices = index.search(q_emb, k)

# #     retrieved_docs = [documents[i] for i in indices[0]]

# #     system_prompt = f"""
# #     You are a senior medical diagnosis specialist for the domain: {domain}.
# #     Always return output in valid JSON with these keys:
# #     - diagnosis
# #     - rationale
# #     - retrieved
# #     """

# #     user_prompt = f"""
# #     Patient data:
# #     {query}

# #     Retrieved medical context:
# #     {retrieved_docs}

# #     Provide the diagnosis JSON.
# #     """

# #     completion = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         temperature=0,
# #         messages=[
# #             {"role": "system", "content": system_prompt},
# #             {"role": "user", "content": user_prompt}
# #         ]
# #     )

# #     return completion.choices[0].message["content"], retrieved_docs
# def rag_query(domain: str, query: str, k=3):
#     # 1. Encode
#     q_emb = embedding_model.encode([query]).astype("float32")
    
#     # 2. Search FAISS
#     scores, indices = index.search(q_emb, k)

#     # Check for index out of bounds (Safety check)
#     valid_indices = [i for i in indices[0] if i < len(documents)]
#     if not valid_indices:
#         print("[WARN] No valid documents found in index.")
#         retrieved_docs = []
#     else:
#         retrieved_docs = [documents[i] for i in valid_indices]

#     system_prompt = f"""
#     You are a senior medical diagnosis specialist for the domain: {domain}.
#     Always return output in valid JSON with these keys:
#     - diagnosis
#     - rationale
#     - retrieved
#     """

#     user_prompt = f"""
#     Patient data:
#     {query}

#     Retrieved medical context:
#     {retrieved_docs}

#     Provide the diagnosis JSON.
#     """

#     # 3. Call OpenAI
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",  
#         temperature=0,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     )

#     # 4. Return Content
#     # <--- FIX 2: Use dot notation (.content) instead of dictionary access ["content"]
#     return completion.choices[0].message.content, retrieved_docs


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("ML Service Ready. FAISS + Embeddings Loaded.")
#     yield


# app = FastAPI(title="BRAINS ML Service", lifespan=lifespan)


# @app.get("/health")
# async def health():
#     return {"status": "ok"}


# # @app.post("/api/retrieve")
# # async def retrieve(req: RetrieveRequest):
# #     try:
# #         results = retrieve_for_patient_text(req.text, k=req.k)
# #         return {"docs": results}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
# @app.post("/api/retrieve")
# async def retrieve(req: RetrieveRequest):
#     try:
#         print(f"\n[DEBUG] Processing Retrieve Request: {req.text[:50]}...")

#         # 1. Generate Embedding (Use the global model loaded at top of main.py)
#         q_emb = embedding_model.encode([req.text]).astype("float32")
        
#         # 2. Search FAISS (Use the global index loaded at top of main.py)
#         scores, indices = index.search(q_emb, req.k)

#         # 3. Retrieve Documents
#         # Validate indices to prevent crashes if index is out of sync
#         valid_indices = [i for i in indices[0] if i < len(documents)]
        
#         results = []
#         for i in valid_indices:
#             # We return the raw text string since that's what build_kb.py saved
#             results.append(documents[i])
            
#         print(f"[DEBUG] Found {len(results)} documents.")
        
#         # Return in the format NestJS expects
#         return {"docs": results}

#     except Exception as e:
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         print("RETRIEVE CRASH DETECTED:")
#         traceback.print_exc() 
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         raise HTTPException(status_code=500, detail=str(e))


# # FIXED: Multi-domain route
# # @app.post("/api/ml/diagnose/{domain}")
# # async def diagnose(domain: str, patient: PatientInput):
# #     try:
# #         patient_query = str(patient)

# #         out, retrieved = rag_query(domain, patient_query)

# #         return {
# #             "diagnosis": out,
# #             "rationale": f"Diagnosis generated for domain '{domain}' using RAG.",
# #             "retrieved": retrieved
# #         }

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/ml/diagnose/{domain}")
# async def diagnose(domain: str, patient: PatientInput):
#     try:
#         # convert patient object to string for RAG query
#         patient_query = f"Age: {patient.age}, Symptoms: {', '.join(patient.symptoms)}"
#         print("\n[DEBUG] Patient Query:", patient_query)

#         raw_llm_output, retrieved = rag_query(domain, patient_query)
#         print("\n[DEBUG] LLM Output:", raw_llm_output)

#         # return {
#         #     "diagnosis": out,
#         #     "rationale": f"Diagnosis generated for domain '{domain}' using RAG.",
#         #     "retrieved": retrieved
#         # }

#         # Remove markdown code blocks (```json and ```)
#         clean_json_text = raw_llm_output.replace("```json", "").replace("```", "").strip()

#         try:
#             # Convert string to Python Dictionary
#             parsed_data = json.loads(clean_json_text)
            
#             final_diagnosis = parsed_data.get("diagnosis", "Unspecified")
#             final_rationale = parsed_data.get("rationale", "No rationale provided.")

#         except json.JSONDecodeError:
#             # Fallback if LLM fails to output valid JSON
#             print("[WARN] LLM did not return valid JSON. Returning raw text.")
#             final_diagnosis = "Parsing Error"
#             final_rationale = clean_json_text

#         # 3. Return Clean Data
#         return {
#             "diagnosis": final_diagnosis,
#             "rationale": final_rationale,
#             "retrieved": retrieved
#         }

#     # except Exception as e:
#     #     raise HTTPException(status_code=500, detail=str(e))
#     except Exception as e:
#         # <--- ADD THIS BLOCK TO SEE THE REAL ERROR IN YOUR TERMINAL
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         print("CRASH DETECTED:")
#         traceback.print_exc() 
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         raise HTTPException(status_code=500, detail=str(e))



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

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
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)