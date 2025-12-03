# ml-service-python\app\agents\domains\cardiology.py
from typing import Dict, Any
from app.diseases import heart_failure, arrhythmia

AGENTS = {"heart_failure": heart_failure.HeartFailureAgent(), "arrhythmia": arrhythmia.ArrhythmiaAgent()}

def select_agent(patient: Dict[str, Any]) -> str:
    return "heart_failure"

def get_agent(name: str):
    return AGENTS[name]