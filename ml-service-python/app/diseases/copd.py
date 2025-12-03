# # ml-service-python\app\diseases\copd.py
# from app.ml_core import brains_retrieval, prompt_builder, llm_connector

# class COPDAgent:
#     def diagnose(self, patient):
#         docs = brains_retrieval.retrieve(patient.get("symptoms",""), k=5)
#         prompt = prompt_builder.build_prompt(patient, docs, disease="COPD")
#         return {"summary": llm_connector.generate(prompt), "evidence": docs}

import os
import json
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

# Import confidence scorer - with fallback
try:
    from ..ml_core.confidence_scorer import calculate_final_confidence
    print("[INFO] COPDAgent: confidence_scorer imported successfully")
except Exception as e:
    print(f"[WARN] COPDAgent: Failed to import confidence_scorer: {e}")
    # Fallback: just use a dummy function
    def calculate_final_confidence(*args, **kwargs):
        return 50  # Default confidence

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
faiss_index_path = Path("data/faiss.index")

documents = []
if faiss_index_path.exists():
    index = faiss.read_index(str(faiss_index_path))
    try:
        with open("data/kb_texts.jsonl", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # skip empty lines
                    continue
                try:
                    doc = json.loads(line)
                    documents.append(doc)
                except json.JSONDecodeError as e:
                    print(f"[WARN] Line {line_num} invalid JSON, skipping: {e}")
                    continue
    except FileNotFoundError:
        print("[WARN] kb_texts.jsonl not found, running without KB")
        index = None
else:
    index = None

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class COPDAgent:
    def __init__(self):
        self.name = "copd"
        self.disease = "Chronic Obstructive Pulmonary Disease"
    
    def diagnose(self, patient):
        """Perform RAG + LLM inference for COPD diagnosis."""
        try:
            # Build query from patient data
            query = " ".join(str(v) for v in patient.values() if v is not None)
            
            # Retrieve relevant documents
            evidence = []
            if index is not None:
                q_emb = embedding_model.encode([query]).astype("float32")
                scores, indices = index.search(q_emb, k=5)
                valid_indices = [i for i in indices[0] if i < len(documents)]
                evidence = [documents[i] for i in valid_indices]
            
            # Build prompt
            system_prompt = f"""
You are an expert pulmonologist specializing in {self.disease}.
Analyze the patient data and provide a structured JSON diagnosis with:
- diagnosis: concise diagnosis statement
- confidence: confidence level (0-100)
- rationale: brief explanation in 3-4 sentences
"""
            
            user_prompt = f"""
Patient Data:
{json.dumps(patient, indent=2)}

Medical Context:
{json.dumps(evidence[:3], indent=2) if evidence else "No relevant documents found"}

Provide diagnosis as valid JSON only.
"""
            
            # Call LLM
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            response_text = completion.choices[0].message.content
            
            # Parse JSON response
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            
            if not clean_json:
                print("[WARN] LLM returned empty response")
                return {
                    "summary": "Unable to provide diagnosis. Please consult a healthcare professional.",
                    "confidence": 0,
                    "rationale": "Insufficient data",
                    "evidence": evidence
                }
            
            try:
                diagnosis_data = json.loads(clean_json)
            except json.JSONDecodeError as json_err:
                print(f"[WARN] JSON parse error: {json_err}. Response was: {clean_json[:200]}")
                diagnosis_data = {
                    "diagnosis": response_text[:200],
                    "rationale": "Response format error"
                }
            
            # Calculate robust confidence score
            llm_stated_confidence = diagnosis_data.get("confidence", None)
            if llm_stated_confidence is not None:
                try:
                    llm_stated_confidence = int(llm_stated_confidence)
                except (ValueError, TypeError):
                    llm_stated_confidence = None
            
            final_confidence = calculate_final_confidence(
                patient_data=patient,
                disease=self.disease,
                diagnosis_text=diagnosis_data.get("diagnosis", ""),
                evidence=evidence,
                llm_confidence_from_response=llm_stated_confidence
            )
            
            return {
                "summary": diagnosis_data.get("diagnosis", "Unable to determine"),
                "confidence": round(final_confidence),
                "rationale": diagnosis_data.get("rationale", ""),
                "evidence": evidence
            }
        
        except Exception as e:
            print(f"[ERROR] COPDAgent.diagnose: {str(e)}")
            return {
                "summary": f"Error: {str(e)}",
                "confidence": 0,
                "rationale": "Diagnosis failed",
                "evidence": []
            }