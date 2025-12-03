# ml-service-python\app\agents\ochestrator\orchestrator.py
# from typing import Dict, Any, Tuple
# from app.agents import neurology, cardiology, pulmonology

# DOMAIN_MAP = {
#     "neurology": neurology,
#     "cardiology": cardiology,
#     "pulmonology": pulmonology,
# }

# KEYWORD_DOMAIN = {
#     "memory": "neurology",
#     "alzheimers": "neurology",
#     "headache": "neurology",
#     "chest": "cardiology",
#     "heart": "cardiology",
#     "breath": "pulmonology",
#     "cough": "pulmonology",
# }

# def choose_domain(patient: Dict[str, Any]) -> str:
#     text = " ".join(str(v) for v in patient.values()).lower()
#     for k, d in KEYWORD_DOMAIN.items():
#         if k in text:
#             return d
#     return "neurology"  # default

# def orchestrate(patient: Dict[str, Any]) -> Dict[str, Any]:
#     domain_key = choose_domain(patient)
#     domain = DOMAIN_MAP.get(domain_key)
#     if domain is None:
#         return {"error": "no domain found"}
#     agent_name = domain.select_agent(patient)
#     # call disease agent
#     agent = domain.get_agent(agent_name)
#     diagnosis = agent.diagnose(patient)
#     return {"domain": domain_key, "agent": agent_name, "diagnosis": diagnosis}

from typing import Dict, Any
from .. import domains

DOMAIN_MAP = {
    "neurology": domains.neurology,
    "cardiology": domains.cardiology,
    "pulmonology": domains.pulmonology,
    "general": domains.general,
}

KEYWORD_DOMAIN_MAP = {
    "memory": "neurology",
    "mmse": "neurology",
    "cdr": "neurology",
    "alzheimer": "neurology",
    "headache": "neurology",
    "stroke": "neurology",
    "chest": "cardiology",
    "heart": "cardiology",
    "cardiac": "cardiology",
    "breath": "pulmonology",
    "cough": "pulmonology",
    "copd": "pulmonology",
    "lung": "pulmonology",
}

DEFAULT_DOMAIN = "general"

def choose_domain(patient: Dict[str, Any]) -> str:
    """Determine domain based on patient data keywords."""
    # Check for explicit domain override
    requested = patient.get("_requested_domain", "").lower().strip()
    
    # Map common aliases to actual domains
    domain_aliases = {
        "chat": "general",
        "assistant": "general",
        "help": "general",
        "unknown": "general",
        "other": "general",
    }
    
    if requested in domain_aliases:
        return domain_aliases[requested]
    
    if requested in DOMAIN_MAP:
        return requested
    
    # Convert patient data to lowercase text
    text = " ".join(str(v).lower() for v in patient.values() if v is not None)
    
    # Score domains by keyword matches
    domain_scores = {d: 0 for d in DOMAIN_MAP.keys()}
    domain_scores.pop("general", None)  # Don't score general domain in auto-detection
    
    for keyword, domain in KEYWORD_DOMAIN_MAP.items():
        if keyword in text:
            domain_scores[domain] += 1
    
    # Return domain with highest score (fallback to general)
    best_domain = max(domain_scores, key=domain_scores.get) if domain_scores else "general"
    return best_domain if domain_scores.get(best_domain, 0) > 0 else DEFAULT_DOMAIN


def orchestrate(patient: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route patient to appropriate domain and disease agent.
    If general query, use the general medical assistant.
    """
    try:
        domain_key = choose_domain(patient)
        print(f"[DEBUG] Orchestrator chose domain: {domain_key}")
        
        domain_module = DOMAIN_MAP.get(domain_key)
        
        if domain_module is None:
            return {
                "error": f"Domain '{domain_key}' not found",
                "domain": domain_key,
                "agent": None,
                "diagnosis": {}
            }
        
        agent_name = domain_module.select_agent(patient)
        print(f"[DEBUG] Domain '{domain_key}' selected agent: {agent_name}")
        
        agent = domain_module.get_agent(agent_name)
        
        if agent is None:
            return {
                "error": f"Agent '{agent_name}' not found in domain '{domain_key}'",
                "domain": domain_key,
                "agent": agent_name,
                "diagnosis": {}
            }
        
        diagnosis = agent.diagnose(patient)
        
        return {
            "domain": domain_key,
            "agent": agent_name,
            "diagnosis": diagnosis,
        }
    
    except Exception as e:
        print(f"[ERROR] Orchestration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "domain": "general",
            "agent": None,
            "diagnosis": {}
        }