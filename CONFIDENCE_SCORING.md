## Confidence Scoring Algorithm

### Overview
The system now calculates **robust medical diagnosis confidence scores** (0-100) by combining multiple independent signals rather than relying solely on the LLM's stated confidence (which was often 0).

### Algorithm Components

#### 1. **Symptom Match Score** (25% weight)
- **Critical symptoms** (70%): Highly specific indicators for the disease
- **Supporting symptoms** (30%): Suggestive but less specific symptoms
- Examples:
  - Alzheimer's critical: "memory loss", "cognitive decline", "confusion"
  - Stroke critical: "facial drooping", "arm weakness", "speech difficulty"
  - COPD critical: "chronic cough", "shortness of breath", "wheezing"

**Scoring**: Matches against disease-specific symptom databases
- Higher score when critical symptoms are present
- Lower score when symptoms are absent or generic

#### 2. **Evidence Quality Score** (20% weight)
- Measures retrieved medical context quality
- Factors:
  - **Document Quantity**: How many relevant documents were retrieved (max 5)
  - **Relevance**: How many patient symptoms appear in the evidence
- Baseline 10% if no evidence available (prevents 0 confidence)

#### 3. **LLM Certainty Extraction** (20% weight)
- Analyzes diagnosis text for confidence keywords without trusting explicit numbers
- **High confidence keywords** (+25 each):
  - "likely", "probable", "consistent with", "pathognomonic"
- **Medium confidence keywords** (+10 each):
  - "may indicate", "could suggest", "possibly"
- **Low confidence keywords** (-10 each):
  - "unclear", "uncertain", "insufficient data"
- Normalized to 0-100 range

#### 4. **Clinical Data Completeness** (15% weight)
- Scored based on patient information provided:
  - Age presence: 25%
  - Symptoms count: 30%
  - Medical history/notes: 20%
  - Additional fields (sex, MMSE, CDR, etc.): 25%
- Complete data = higher confidence (doctor has more to work with)
- Missing data = lower confidence (more uncertainty)

#### 5. **Disease-Specific Rules** (20% weight)
- Domain-specific scoring adjustments:
  - **Alzheimer's**: +15 for age ≥65, +10 for cognitive symptoms
  - **Stroke**: +20 for acute symptom keywords
  - **COPD**: +15 for smoking history, +10 for respiratory symptoms
  - **Heart Failure**: +10 for age ≥55, +15 for cardiac risk factors
  - **Brain Tumor**: +15 for neurological symptoms

### Final Calculation

```
Final Score = (
    Symptom_Match × 0.25 +
    Evidence_Quality × 0.20 +
    LLM_Certainty × 0.20 +
    Clinical_Completeness × 0.15 +
    Disease_Specific × 0.20
)
```

### Sanity Checks Applied
- If no symptoms AND no evidence → cap at 40% (too uncertain)
- If ≥2 critical symptoms AND ≥3 documents → boost by 10% (strong case)
- If LLM provided explicit confidence → blend with calculated score (60% algorithm, 40% LLM)

### Example Scenarios

**Scenario 1: Strong Case**
- 74-year-old patient with memory loss + confusion
- 3 relevant documents retrieved about Alzheimer's
- LLM response: "Highly consistent with Alzheimer's disease"
- Result: ~75-85 confidence

**Scenario 2: Weak Case**
- Patient with vague "feeling tired"
- No specific medical symptoms
- No documents retrieved
- LLM response: "Cannot determine from available data"
- Result: ~20-35 confidence

**Scenario 3: Incomplete Data**
- Clear symptoms present
- Good evidence retrieved
- But patient age/history missing
- Result: ~50-65 confidence (data completeness penalty)

### Debug Logging
Every diagnosis logs detailed confidence breakdown:
```
[CONFIDENCE] Disease=Alzheimer's disease | 
    SymptomMatch=82.5 | 
    Evidence=75.0 | 
    LLMCertainty=68.5 | 
    Completeness=60.0 | 
    DiseaseScore=65.0 | 
    Final=72.4
```

### Integration Points
- All disease agents use this module
- Called after LLM diagnosis generation
- Output returned in diagnosis response
- Frontend displays confidence as a percentage (0-100)

### Future Improvements
1. Add patient outcome tracking to validate scores
2. Implement dynamic weighting based on model performance
3. Add confidence intervals (e.g., 72±5%)
4. Include external clinical guideline alignment scores
5. Add temporal trend analysis (improving/declining confidence over multiple queries)
