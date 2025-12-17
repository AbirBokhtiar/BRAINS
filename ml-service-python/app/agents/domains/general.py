# from ....app import diseases
import numpy as np

class GeneralMedicalAssistant:
    """Generic medical assistant for general queries (chat mode)."""
    def __init__(self):
        self.name = "general_medical_assistant"
        self.disease = "General Medical Query"
    
    def diagnose(self, patient):
        """Provide general medical guidance using RAG without disease-specific routing."""
        return self.provide_guidance(patient)
    
    def provide_guidance(self, patient):
        """RAG-based medical guidance for general queries."""
        import os
        import json
        from openai import OpenAI
        from sentence_transformers import SentenceTransformer
        import faiss
        from pathlib import Path
        
        # Import confidence scorer - with fallback
        try:
            from ...ml_core.confidence_scorer import calculate_final_confidence
        except Exception as e:
            print(f"[WARN] GeneralMedicalAssistant: Failed to import confidence_scorer: {e}")
            # Fallback: just use a dummy function
            def calculate_final_confidence(*args, **kwargs):
                return 50  # Default confidence
        
        # embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        # --- FIX START ---
        from google import genai

        # 1. Rename to 'gemini_client' to avoid conflict with OpenAI 'client'
        gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        def get_gemini_embedding(text: str) -> list[float]:
            """
            Generate embeddings using Gemini API via google-genai.
            """
            try:
                # 2. Update model to a valid path (often 'models/' prefix is safer)
                # 3. Use 'gemini_client' here
                response = gemini_client.models.embed_content(
                    model="models/text-embedding-004", # Updated to latest stable model
                    contents=[text]
                )
                # 4. Handle response structure safely
                if response.embeddings:
                    return response.embeddings[0].values
                else:
                    raise ValueError("No embedding returned from Gemini API")
                    
            except AttributeError:
                # Fallback for different SDK versions returning object vs dict
                return response.embeddings[0]
            except Exception as e:
                print(f"[ERROR] Gemini Embedding Failed: {e}")
                # Fallback to zero vector to prevent crash if API fails
                return [0.0] * 768 

        # --- FIX END ---

        embedding_cache = {}

        def get_embedding_cached(text):
            # Turn list input into a single key
            key = " ".join(text) if isinstance(text, list) else str(text)

            if key in embedding_cache:
                return embedding_cache[key]

            emb = get_gemini_embedding(key)
            embedding_cache[key] = emb
            return emb


        class EmbeddingModelWrapper:
            def encode(self, texts, batch_size=32):
                embeddings = []
                for text in texts:
                    emb = get_embedding_cached(text)
                    embeddings.append(emb)
                return np.array(embeddings, dtype="float32")
            
        embedding_model = EmbeddingModelWrapper()

        faiss_index_path = Path("data/faiss.index")
        
        # Load documents
        documents = []
        try:
            with open("data/kb_texts.jsonl", "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        doc = json.loads(line)
                        documents.append(doc)
                    except json.JSONDecodeError as e:
                        print(f"[WARN] kb_texts.jsonl line {line_num} invalid JSON, skipping: {e}")
                        continue
        except FileNotFoundError:
            print("[WARN] kb_texts.jsonl not found")
            documents = []
        
        # Load FAISS index
        index = None
        if faiss_index_path.exists() and len(documents) > 0:
            index = faiss.read_index(str(faiss_index_path))
        
        # Build query
        query = " ".join(str(v) for v in patient.values() if v is not None)
        
        # Retrieve relevant documents
        evidence = []
        if index is not None and len(documents) > 0:
            q_emb = embedding_model.encode([query]).astype("float32")
            scores, indices = index.search(q_emb, k=5)
            valid_indices = [i for i in indices[0] if 0 <= i < len(documents)]
            evidence = [documents[i] for i in valid_indices]
        
        # LLM call
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        system_prompt = """
You are a knowledgeable and empathetic medical assistant. 
You provide general medical guidance based on the patient's symptoms.

IMPORTANT: You MUST respond with ONLY a valid JSON object (no markdown, no code blocks, just raw JSON).
The JSON must have exactly these fields:
{
  "diagnosis": "concise medical guidance or possible conditions (string)",
  "confidence": 50,
  "rationale": "brief explanation of your assessment (string)"
}

Guidelines:
- Never assert a definitive diagnosis
- check for symptoms and suggest possible conditions and suggest a course of action
- Always recommend consulting a healthcare professional(be specific for who to consult if possible)
- Provide evidence-based information when possible
- Be clear: "I'm an AI assistant, not a professional"
- Flag emergency symptoms (chest pain, severe headache, etc.)
- Keep responses clear and concise
"""
        
        user_prompt = f"""
Patient Query:
{json.dumps(patient, indent=2)}

Available Medical Context:
{json.dumps(evidence[:3], indent=2) if evidence else "General medical knowledge available"}

Please provide helpful, accurate medical information. Be conversational and supportive.
"""
        
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.5,  # slightly higher for conversational tone
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            response_text = completion.choices[0].message.content
            print(f"[DEBUG] GeneralMedicalAssistant LLM response: {response_text[:200]}")

            # Parse JSON response
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            
            # Ensure clean_json is not empty
            if not clean_json:
                print("[WARN] LLM returned empty response, using fallback")
                return {
                    "summary": "I need more information to provide guidance. Please describe your symptoms in detail.",
                    "mode": "general_medical_assistant",
                    "conversational": True,
                    "confidence": 0,
                    "rationale": "Insufficient data",
                    "evidence": evidence,
                    "recommendation": "Please consult with a healthcare professional for proper diagnosis and treatment."
                }
            
            try:
                diagnosis_data = json.loads(clean_json)
            except json.JSONDecodeError as json_err:
                print(f"[WARN] JSON parse error: {json_err}. Response was: {clean_json[:400]}")
                # Fallback: treat response as plain text
                diagnosis_data = {
                    "diagnosis": response_text[:200],
                    "rationale": "Response could not be parsed as structured JSON"
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
                "mode": "general_medical_assistant",
                "conversational": True,
                "confidence": round(final_confidence),
                "rationale": diagnosis_data.get("rationale", ""),
                "evidence": evidence,
                "recommendation": "Please consult with a healthcare professional for proper diagnosis and treatment."
            }
        
        except Exception as e:
            print(f"[ERROR] GeneralMedicalAssistant.provide_guidance: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "summary": "I encountered an error processing your request. Please try again or consult a healthcare professional.",
                "mode": "general_assistant",
                "conversational": True,
                "confidence": 0,
                "evidence": [],
                "recommendation": "Please consult with a healthcare professional."
            }


# Singleton instance
_general_assistant = GeneralMedicalAssistant()


def select_agent(patient):
    """Always return the general medical assistant for general queries."""
    return "general_medical_assistant"


def get_agent(name):
    """Get the general medical assistant agent."""
    if name == "general_medical_assistant":
        return _general_assistant
    return None