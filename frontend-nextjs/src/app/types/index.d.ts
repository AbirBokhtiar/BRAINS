export type Domain = 'cardiology' | 'neurology' | 'pulmonology' | 'general';


export interface PatientPayload {
    // id?: string;
    // name?: string;
    age: number;
    symptoms: string | string[];
    imageBase64?: string | null;
}


export interface DiagnosisResult {
    diagnosis?: string;
    rationale?: string;
    retrieved?: string[];
    condition?: string;
    confidence?: number;
    recommendation?: string;
}