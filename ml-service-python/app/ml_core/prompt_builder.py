# ml-service-python\app\ml_core\prompt_builder.py
from typing import Dict, List

def build_prompt(patient: Dict, docs: List[Dict], disease: str) -> str:
    pieces = [f"Patient data: {patient}\n"]
    pieces.append(f"Target disease: {disease}\n")
    pieces.append("Relevant knowledge:\n")
    for d in docs:
        pieces.append(f"- {d.get('text', '')[:500]}\n")
    pieces.append("\nPlease provide a concise diagnostic summary (probabilities, rationale, recommended next steps).")
    return "\n".join(pieces)