# # ml-service-python/data/generate_synthetic.py
# import json
# import random
# from pathlib import Path

# OUT = Path(__file__).parent / "kb_texts.jsonl"

# diagnoses = [
#     "Normal cognition",
#     "Very Mild Alzheimer's Disease",
#     "Mild Alzheimer's Disease",
#     "Moderate Alzheimer's Disease",
#     "Severe Alzheimer's Disease"
# ]

# apoe_choices = ["e3/e3", "e3/e4", "e4/e4", "e2/e3"]
# sex_choices = ["M", "F"]

# def gen_case(i):
#     age = random.randint(55, 90)
#     mmse = max(0, min(30, int(random.gauss(24 - (age-70)/6, 3))))
#     cdr = round(min(3, max(0, random.choice([0,0.5,1,2,3]) if mmse < 26 else 0)),1)
#     etiv = int(random.gauss(1500, 80))
#     nwbv = round(max(0.5, min(0.9, random.gauss(0.70 - (age-65)/300, 0.04))), 3)
#     apoe = random.choice(apoe_choices)
#     sex = random.choice(sex_choices)
#     # map mmse -> coarse diagnosis
#     if mmse >= 27:
#         diag = "Normal cognition"
#     elif mmse >= 24:
#         diag = "Very Mild Alzheimer's Disease"
#     elif mmse >= 20:
#         diag = "Mild Alzheimer's Disease"
#     elif mmse >= 14:
#         diag = "Moderate Alzheimer's Disease"
#     else:
#         diag = "Severe Alzheimer's Disease"

#     text = (
#         f"CaseID: {i}. Age: {age} years, Sex: {sex}, MMSE: {mmse}, CDR: {cdr}, "
#         f"eTIV: {etiv} mL, nWBV: {nwbv}. APOE: {apoe}. Outcome: {diag}."
#     )
#     return {"case_id": f"case_{i:05d}", "text": text, "age": age, "mmse": mmse, "cdr": cdr, "diag": diag}

# def main(n=2000):
#     OUT.parent.mkdir(parents=True, exist_ok=True)
#     with OUT.open("w", encoding="utf8") as f:
#         for i in range(1, n+1):
#             case = gen_case(i)
#             f.write(json.dumps(case, ensure_ascii=False) + "\n")
#     print(f"Wrote {n} cases to {OUT}")

# if __name__ == "__main__":
#     main(2000)


# ml-service-python/data/generate_synthetic.py
"""
Generate synthetic medical knowledge-base entries for
multi-domain, multi-disease BRAINS diagnostic system.

Output:
    data/kb_texts.jsonl  → one JSON document per line, each containing:
        {
            "case_id": "...",
            "domain": "neurology | cardiology | pulmonology",
            "subdomain": "...",
            "text": "... long sentence the RAG uses",
            ... optional numeric features ...
        }
"""

import json
import random
from pathlib import Path

OUT = Path(__file__).parent / "kb_texts.jsonl"


# ---------------------------------------------------------
# 1. Define domains and sub-domains for multi-agent system
# ---------------------------------------------------------
DOMAINS = {
    "neurology": [
        "alzheimers",
        "brain_tumor",
        "stroke"
    ],
    "cardiology": [
        "heart_failure",
        "arrhythmia",
        "hypertension"
    ],
    "pulmonology": [
        "asthma",
        "copd",
        "pneumonia"
    ]
}


# ---------------------------------------------------------
# 2. Synthetic parameter generators for realism
# ---------------------------------------------------------
sex_choices = ["M", "F"]
apoe_choices = ["e3/e3", "e3/e4", "e4/e4", "e2/e3"]

def bounded(value, lo, hi):
    return min(hi, max(lo, value))


# ---------------------------------------------------------
# 3. Disease-specific synthetic logic
# ---------------------------------------------------------
def generate_neurology_case(sub, i):
    age = random.randint(55, 90)
    mmse = bounded(int(random.gauss(26, 4)), 0, 30)
    cdr = bounded(round(random.choice([0, 0.5, 1, 2, 3]), 1), 0, 3)
    etiv = int(random.gauss(1500, 80))
    nwbv = bounded(round(random.gauss(0.72, 0.03), 3), 0.55, 0.90)
    apoe = random.choice(apoe_choices)
    sex = random.choice(sex_choices)

    # Label based on mmse
    if mmse >= 27:
        diag = "Normal cognition"
    elif mmse >= 24:
        diag = "Very Mild Alzheimer's Disease"
    elif mmse >= 20:
        diag = "Mild Alzheimer's Disease"
    elif mmse >= 14:
        diag = "Moderate Alzheimer's Disease"
    else:
        diag = "Severe Alzheimer's Disease"

    text = (
        f"Domain: Neurology. Subdomain: {sub}. CaseID {i}. "
        f"Age {age}, Sex {sex}. MMSE score {mmse}, CDR {cdr}, "
        f"eTIV {etiv} mL, nWBV {nwbv}. APOE genotype {apoe}. "
        f"Outcome: {diag}."
    )

    return {
        "case_id": f"neuro_{i:05d}",
        "domain": "neurology",
        "subdomain": sub,
        "text": text,
        "age": age,
        "mmse": mmse,
        "cdr": cdr,
        "etiv": etiv,
        "nwbv": nwbv,
        "apoe": apoe,
        "diagnosis_label": diag
    }


def generate_cardiology_case(sub, i):
    age = random.randint(40, 90)
    heart_rate = random.randint(60, 130)
    bp_sys = random.randint(110, 180)
    bp_dia = random.randint(70, 110)
    cholesterol = random.randint(160, 280)
    sex = random.choice(sex_choices)

    if bp_sys > 150:
        diag = "Uncontrolled hypertension"
    elif heart_rate > 110:
        diag = "Possible arrhythmia"
    else:
        diag = "Stable cardiovascular profile"

    text = (
        f"Domain: Cardiology. Subdomain: {sub}. CaseID {i}. "
        f"Age {age}, Sex {sex}. "
        f"Heart rate {heart_rate} bpm, BP {bp_sys}/{bp_dia} mmHg, "
        f"Cholesterol {cholesterol} mg/dL. Outcome: {diag}."
    )

    return {
        "case_id": f"cardio_{i:05d}",
        "domain": "cardiology",
        "subdomain": sub,
        "text": text,
        "age": age,
        "heart_rate": heart_rate,
        "bp_sys": bp_sys,
        "bp_dia": bp_dia,
        "cholesterol": cholesterol,
        "diagnosis_label": diag
    }


def generate_pulmonology_case(sub, i):
    age = random.randint(20, 90)
    spo2 = random.randint(85, 99)
    fev1 = round(random.uniform(1.0, 4.0), 2)
    cough = random.choice(["mild", "moderate", "severe"])
    fever = random.choice([True, False])
    sex = random.choice(sex_choices)

    if spo2 < 90 and fev1 < 1.5:
        diag = "Severe COPD exacerbation"
    elif fever and cough == "severe":
        diag = "Likely infectious pneumonia"
    else:
        diag = "Stable pulmonary condition"

    text = (
        f"Domain: Pulmonology. Subdomain: {sub}. CaseID {i}. "
        f"Age {age}, Sex {sex}. SPO2 {spo2}%, FEV1 {fev1} L, "
        f"Cough severity {cough}, Fever {fever}. "
        f"Outcome: {diag}."
    )

    return {
        "case_id": f"pulmo_{i:05d}",
        "domain": "pulmonology",
        "subdomain": sub,
        "text": text,
        "age": age,
        "spo2": spo2,
        "fev1": fev1,
        "cough": cough,
        "fever": fever,
        "diagnosis_label": diag
    }


# Mapping for dynamic generation
GENERATOR = {
    "neurology": generate_neurology_case,
    "cardiology": generate_cardiology_case,
    "pulmonology": generate_pulmonology_case,
}


# ---------------------------------------------------------
# 4. Main generator
# ---------------------------------------------------------
def main(n_per_subdomain=500):
    OUT.parent.mkdir(exist_ok=True, parents=True)

    with OUT.open("w", encoding="utf-8") as f:
        for domain, subs in DOMAINS.items():
            for sub in subs:
                generator = GENERATOR[domain]
                for i in range(1, n_per_subdomain + 1):
                    case = generator(sub, i)
                    f.write(json.dumps(case, ensure_ascii=False) + "\n")

    print(f"Generated ~{n_per_subdomain * sum(len(v) for v in DOMAINS.values())} KB entries into {OUT}")


if __name__ == "__main__":
    main(n_per_subdomain=500)
