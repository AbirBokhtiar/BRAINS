# ml-service-python/app/schemas.py
# from pydantic import BaseModel
# from typing import Optional, List

# class PatientInput(BaseModel):
#     age: Optional[int]
#     sex: Optional[str]
#     mmse: Optional[float]
#     cdr: Optional[float]
#     etiv: Optional[float]
#     nwbv: Optional[float]
#     apoe: Optional[str]
#     notes: Optional[str] = ""

# class RetrieveRequest(BaseModel):
#     text: str
#     k: int = 5

# class DiagnosisResponse(BaseModel):
#     diagnosis: str
#     rationale: str
#     retrieved: List[dict]

from pydantic import BaseModel
from typing import List, Optional, Union

class PatientInput(BaseModel):
    age: int
    symptoms: Union[str, List[str]]  # Accept both string and list of strings

class RetrieveRequest(BaseModel):
    text: str
    k: int = 5

class DiagnosisResponse(BaseModel):
    diagnosis: str
    rationale: str
    retrieved: List[dict]
    confidence: Optional[float] = None
    scores: Optional[dict] = None
