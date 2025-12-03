"""
Confidence Scoring Module for Medical Diagnoses

Combines multiple signals to produce a reliable confidence score (0-100):
1. Symptom Match Score: How well patient symptoms align with the disease
2. Retrieved Context Quality: Relevance and quantity of supporting evidence
3. LLM Certainty Signals: Keywords indicating confidence in the response
4. Clinical Data Completeness: How much patient history/data was provided
5. Disease-Specific Scoring: Domain-specific risk factors and indicators
"""

import json
import re
from typing import Dict, List, Any, Tuple


# Disease-specific symptom mappings for scoring
DISEASE_SYMPTOM_MAP = {
    "alzheimers": {
        "critical": ["memory loss", "cognitive decline", "confusion", "dementia"],
        "supporting": ["disorientation", "language difficulty", "personality change", "depression"],
        "weight": 0.3
    },
    "stroke": {
        "critical": ["facial drooping", "arm weakness", "speech difficulty", "numbness"],
        "supporting": ["sudden onset", "headache", "vision loss", "dizziness"],
        "weight": 0.3
    },
    "copd": {
        "critical": ["chronic cough", "shortness of breath", "wheezing", "dyspnea"],
        "supporting": ["smoking history", "emphysema", "bronchitis", "chest pain"],
        "weight": 0.3
    },
    "heart_failure": {
        "critical": ["shortness of breath", "fatigue", "edema", "chest pain"],
        "supporting": ["hypertension", "heart attack history", "arrhythmia", "palpitations"],
        "weight": 0.3
    },
    "brain_tumor": {
        "critical": ["headache", "vision changes", "seizures", "nausea"],
        "supporting": ["cognitive changes", "balance issues", "weakness", "speech problems"],
        "weight": 0.3
    },
    "general": {
        "critical": ["symptoms", "patient"],
        "supporting": [],
        "weight": 0.2
    }
}

# LLM certainty keywords that indicate high confidence
HIGH_CONFIDENCE_KEYWORDS = [
    "likely", "probable", "consistent with", "classic presentation",
    "typical", "diagnostic criteria", "evidence-based", "strongly suggest",
    "clearly", "definite", "confirmed", "pathognomonic"
]

MEDIUM_CONFIDENCE_KEYWORDS = [
    "may indicate", "could suggest", "possibly", "consider",
    "potential", "differential", "features suggest"
]

LOW_CONFIDENCE_KEYWORDS = [
    "unclear", "uncertain", "inconclusive", "rule out",
    "cannot determine", "insufficient", "limited data"
]


def calculate_symptom_match_score(
    patient_symptoms: List[str],
    disease: str
) -> Tuple[float, int]:
    """
    Calculate symptom match score based on disease-specific symptom mappings.
    
    Returns:
        Tuple of (score 0-100, matched_count)
    """
    if not patient_symptoms:
        return 0.0, 0
    
    disease_key = disease.lower().replace(" ", "_").replace("'s", "")
    symptom_map = DISEASE_SYMPTOM_MAP.get(disease_key, DISEASE_SYMPTOM_MAP["general"])
    
    symptoms_text = " ".join(str(s).lower() for s in patient_symptoms)
    
    critical_matches = 0
    supporting_matches = 0
    
    # Check critical symptoms
    for symptom in symptom_map.get("critical", []):
        if symptom.lower() in symptoms_text:
            critical_matches += 1
    
    # Check supporting symptoms
    for symptom in symptom_map.get("supporting", []):
        if symptom.lower() in symptoms_text:
            supporting_matches += 1
    
    # Score: critical symptoms weighted more heavily
    total_critical = len(symptom_map.get("critical", []))
    total_supporting = len(symptom_map.get("supporting", []))
    
    critical_score = (critical_matches / total_critical * 100) if total_critical > 0 else 0
    supporting_score = (supporting_matches / total_supporting * 100) if total_supporting > 0 else 0
    
    # Weight: critical 70%, supporting 30%
    symptom_score = (critical_score * 0.7) + (supporting_score * 0.3)
    
    return symptom_score, critical_matches + supporting_matches


def calculate_evidence_quality_score(
    evidence: List[Dict[str, Any]],
    patient_symptoms: List[str]
) -> float:
    """
    Score quality and relevance of retrieved medical context.
    
    Factors:
    - Quantity of retrieved documents
    - Relevance (how much they mention patient symptoms)
    - Recency/authority of sources (if available)
    """
    if not evidence:
        return 10.0  # Small baseline for no evidence
    
    max_docs = 5
    doc_count_score = min(len(evidence) / max_docs * 100, 100)
    
    # Calculate relevance by checking how many symptoms appear in evidence
    evidence_text = " ".join(
        str(doc.get("content", "")) + " " + str(doc.get("title", ""))
        for doc in evidence
    ).lower()
    
    if not patient_symptoms:
        relevance_score = 30.0  # Low relevance if no symptoms to match
    else:
        symptom_hits = sum(
            1 for symptom in patient_symptoms
            if str(symptom).lower() in evidence_text
        )
        relevance_score = (symptom_hits / len(patient_symptoms)) * 100
    
    # Combined: doc count (40%) + relevance (60%)
    quality_score = (doc_count_score * 0.4) + (relevance_score * 0.6)
    
    return min(quality_score, 100.0)


def extract_llm_certainty_score(diagnosis_text: str) -> float:
    """
    Extract confidence signals from LLM diagnosis text.
    
    Uses keyword matching to gauge LLM certainty without relying solely
    on an explicit confidence number (which the LLM might get wrong).
    """
    text_lower = diagnosis_text.lower()
    
    high_count = sum(1 for kw in HIGH_CONFIDENCE_KEYWORDS if kw in text_lower)
    medium_count = sum(1 for kw in MEDIUM_CONFIDENCE_KEYWORDS if kw in text_lower)
    low_count = sum(1 for kw in LOW_CONFIDENCE_KEYWORDS if kw in text_lower)
    
    # Scoring: high=+25, medium=+10, low=-10 per occurrence
    certainty_score = (high_count * 25) + (medium_count * 10) - (low_count * 10)
    
    # Normalize to 0-100 range
    certainty_score = max(0, min(100, 50 + certainty_score))  # Center around 50
    
    return certainty_score


def calculate_clinical_completeness_score(patient_data: Dict[str, Any]) -> float:
    """
    Score based on how complete the patient data is.
    
    Factors:
    - Presence of age
    - Presence of symptoms
    - Presence of medical history
    - Number of non-null fields
    """
    completeness = 0.0
    max_completeness = 0.0
    
    # Age presence (important for risk assessment)
    if patient_data.get("age"):
        completeness += 25
    max_completeness += 25
    
    # Symptoms presence (critical for diagnosis)
    symptoms = patient_data.get("symptoms", [])
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.split(",") if s.strip()]
    
    if symptoms and len(symptoms) > 0:
        symptom_count_score = min((len(symptoms) / 5) * 30, 30)
        completeness += symptom_count_score
    max_completeness += 30
    
    # Medical history/notes
    notes = patient_data.get("notes") or patient_data.get("medical_history", "")
    if notes and len(str(notes).strip()) > 10:
        completeness += 20
    max_completeness += 20
    
    # Additional fields (sex, mmse, cdr, etc.)
    additional_fields = ["sex", "mmse", "cdr", "etiv", "nwbv", "apoe"]
    additional_filled = sum(1 for field in additional_fields if patient_data.get(field))
    if additional_filled > 0:
        additional_score = min((additional_filled / len(additional_fields)) * 25, 25)
        completeness += additional_score
    max_completeness += 25
    
    # Normalize
    final_score = (completeness / max_completeness * 100) if max_completeness > 0 else 0
    return min(final_score, 100.0)


def calculate_disease_specific_score(
    patient_data: Dict[str, Any],
    disease: str
) -> float:
    """
    Apply disease-specific scoring rules based on clinical indicators.
    """
    age = patient_data.get("age")
    symptoms = patient_data.get("symptoms", [])
    
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.split(",") if s.strip()]
    
    disease_key = disease.lower().replace(" ", "_").replace("'s", "")
    score = 50.0  # Baseline
    
    # Alzheimer's: higher score for older age + cognitive symptoms
    if disease_key == "alzheimers":
        if age and age >= 65:
            score += 15
        if any(s in str(symptoms).lower() for s in ["memory", "cognitive", "confusion"]):
            score += 10
    
    # Stroke: presence of acute symptoms
    elif disease_key == "stroke":
        if any(s in str(symptoms).lower() for s in ["sudden", "acute", "facial", "speech", "weakness"]):
            score += 20
    
    # COPD: smoking history + respiratory symptoms
    elif disease_key == "copd":
        if any(s in str(symptoms).lower() for s in ["smoking", "pack-years"]):
            score += 15
        if any(s in str(symptoms).lower() for s in ["cough", "breath", "wheeze"]):
            score += 10
    
    # Heart Failure: age + cardiac risk factors
    elif disease_key == "heart_failure":
        if age and age >= 55:
            score += 10
        if any(s in str(symptoms).lower() for s in ["hypertension", "diabetes", "heart"]):
            score += 15
    
    # Brain Tumor: neurological symptoms
    elif disease_key == "brain_tumor":
        if any(s in str(symptoms).lower() for s in ["headache", "seizure", "vision", "balance"]):
            score += 15
    
    return min(score, 100.0)


def calculate_final_confidence(
    patient_data: Dict[str, Any],
    disease: str,
    diagnosis_text: str,
    evidence: List[Dict[str, Any]],
    llm_confidence_from_response: int = None
) -> float:
    """
    Calculate comprehensive confidence score by combining multiple factors.
    
    Args:
        patient_data: Patient information
        disease: Disease being diagnosed
        diagnosis_text: Text of the LLM diagnosis
        evidence: Retrieved medical evidence
        llm_confidence_from_response: Explicit confidence from LLM (if provided)
    
    Returns:
        Final confidence score (0-100)
    """
    
    # Extract components
    symptoms = patient_data.get("symptoms", [])
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.split(",") if s.strip()]
    
    symptom_match_score, matched_count = calculate_symptom_match_score(symptoms, disease)
    evidence_score = calculate_evidence_quality_score(evidence, symptoms)
    llm_certainty_score = extract_llm_certainty_score(diagnosis_text)
    completeness_score = calculate_clinical_completeness_score(patient_data)
    disease_score = calculate_disease_specific_score(patient_data, disease)
    
    # If LLM provided explicit confidence, validate it against our signals
    if llm_confidence_from_response is not None:
        llm_confidence_from_response = max(0, min(100, llm_confidence_from_response))
    
    # Weighted average of all factors
    weights = {
        "symptom_match": 0.25,
        "evidence": 0.20,
        "llm_certainty": 0.20,
        "completeness": 0.15,
        "disease_specific": 0.20
    }
    
    final_score = (
        (symptom_match_score * weights["symptom_match"]) +
        (evidence_score * weights["evidence"]) +
        (llm_certainty_score * weights["llm_certainty"]) +
        (completeness_score * weights["completeness"]) +
        (disease_score * weights["disease_specific"])
    )
    
    # Adjust based on LLM's stated confidence if available
    if llm_confidence_from_response is not None:
        # Average with our calculated score (trust LLM but verify)
        final_score = (final_score * 0.6) + (llm_confidence_from_response * 0.4)
    
    # Apply sanity checks
    # If very few symptoms and no evidence, cap confidence
    if matched_count == 0 and len(evidence) == 0:
        final_score = min(final_score, 40.0)
    
    # If good evidence and symptom match, boost slightly
    if matched_count >= 2 and len(evidence) >= 3:
        final_score = min(final_score + 10, 100.0)
    
    # Debug logging
    print(f"[CONFIDENCE] Disease={disease} | "
          f"SymptomMatch={symptom_match_score:.1f} | "
          f"Evidence={evidence_score:.1f} | "
          f"LLMCertainty={llm_certainty_score:.1f} | "
          f"Completeness={completeness_score:.1f} | "
          f"DiseaseScore={disease_score:.1f} | "
          f"Final={final_score:.1f}")
    
    return min(max(final_score, 0), 100)
