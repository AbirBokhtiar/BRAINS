# ml-service-python\app\agents\domains\pulmonology.py
from typing import Dict, Any
from app.diseases import copd

AGENTS = {"copd": copd.COPDAgent()}

def select_agent(patient: Dict[str, Any]) -> str:
    return "copd"

def get_agent(name: str):
    return AGENTS[name]