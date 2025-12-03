# ml-service-python\app\agents\domains\neurology.py
from typing import Dict, Any
from app.diseases import alzheimers, brain_tumor, stroke

AGENTS = {
    "alzheimers": alzheimers.AlzheimersAgent(),
    "brain_tumor": brain_tumor.BrainTumorAgent(),
    "stroke": stroke.StrokeAgent(),
}

def select_agent(patient: Dict[str, Any]) -> str:
    text = " ".join(str(v) for v in patient.values()).lower()
    if "memory" in text or "mmse" in text:
        return "alzheimers"
    if "tumor" in text or "mass" in text:
        return "brain_tumor"
    if "stroke" in text or "weak" in text:
        return "stroke"
    if "alzheimer" in text or "dementia" in text:
        return "alzheimers"
    return "alzheimers"

def get_agent(name: str):
    return AGENTS[name]