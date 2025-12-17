import { DiagnosisResult, PatientPayload } from '@/app/types';


const NEST_BASE = process.env.BACKEND_URL || 'http://localhost:4000';

export async function postDiagnosis(domain: string, sub: string, payload: PatientPayload): Promise<DiagnosisResult> {
    const res = await fetch(`${NEST_BASE}/agents/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain, patient: payload }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}

// export async function askAssistant(domain: string, message: string): Promise<{ reply: string }> {
//     const res = await fetch(`${NEST_BASE}/agents/run`, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ domain: 'general', message }),
//     });
//     if (!res.ok) throw new Error(await res.text());
//     return res.json();
// }


export async function askAssistant(domain: string, query: string) {
  try {
    const response = await fetch(`${NEST_BASE}/agents/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        domain: domain,
        patient: { symptoms: query }, 
        k: 3 
      }),
    });

    if (!response.ok) {
        throw new Error(`Server Error: ${response.statusText}`);
    }

    // 1. Parse JSON exactly once
    const data = await response.json();

    // 2. Extract the answer correctly based on the flattened backend structure
    // We prefer 'recommendation' (rationale), then 'condition' (diagnosis)
    const answer = data.recommendation || data.condition || "I couldn't find a specific answer in the medical records.";
    
    return { reply: answer };

  } catch (error) {
    console.error("Chat Error:", error);
    throw new Error("Failed to reach the medical assistant.");
  }
}