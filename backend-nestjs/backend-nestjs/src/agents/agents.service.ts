import { Injectable, Logger } from '@nestjs/common';
import { MlGatewayService } from '../ml/ml.service';

export type AgentDomain = 'cardiology' | 'neurology' | 'pulmonology' | 'general';

@Injectable()
export class AgentsService {
  private readonly logger = new Logger(AgentsService.name);

  constructor(private readonly mlService: MlGatewayService) {}

  // simple router logic to pick domain-specific prompt templates
  private domainSystemPrompt(domain: AgentDomain) {
    switch (domain) {
      case 'cardiology':
        return 'You are a cardiology diagnostic assistant. Focus on heart-related differentials.';
      case 'neurology':
        return 'You are a neurology diagnostic assistant. Focus on neurologic differentials.';
      case 'pulmonology':
        return 'You are a pulmonology diagnostic assistant. Focus on respiratory system differentials.';
      case 'general':
        return 'You are a general medical diagnostic assistant.'
      default:
        return 'You are a general medical diagnostic assistant.';
    }
  }

  // orchestrate retrieval + diagnosis
  // async runAgent(domain: AgentDomain, patient: any, k = 5) {
  //   // 1) Retrieve relevant docs from Python ML service
  //   this.logger.debug(`Running retrieval for domain=${domain}`);
  //   const queryText = patient.symptoms ?? JSON.stringify(patient);
  //   const retrieved = await this.mlService.retrieveText(queryText, k);

  //   // 2) Build prompt to send for diagnosis (the Python ML service handles RAG if you like)
  //   const systemPrompt = this.domainSystemPrompt(domain);
  //   const combined = {
  //     ...patient,
  //     retrieved: retrieved?.docs ?? retrieved, // accept either shape
  //     // system_prompt: systemPrompt,
  //   };
  //   // const combined = {
  //   //   age: patient.age ?? null,
  //   //   sex: patient.sex ?? null,
  //   //   mmse: patient.mmse ?? null,
  //   //   cdr: patient.cdr ?? null,
  //   //   etiv: patient.etiv ?? null,
  //   //   nwbv: patient.nwbv ?? null,
  //   //   apoe: patient.apoe ?? null,
  //   //   notes: patient.notes ?? patient.symptoms ?? ""
  //   // };


  //   // 3) Call diagnose endpoint (Python ML)
  //   this.logger.debug('Calling ML diagnose endpoint');
  //   const diagnosis = await this.mlService.sendDiagnosisRequest(domain, combined);

  //   // 4) Normalize/return
  //   return {
  //     domain,
  //     retrieved: retrieved?.docs ?? retrieved,
  //     diagnosis,
  //   };
  // }

  async runAgent(domain: AgentDomain, patient: any, k = 5) {
    if (!patient) {
        patient = { symptoms: "No symptoms provided", age: 0 };
    }
    // 1) Retrieve relevant docs (Optional: The Python service does this internally anyway based on main.py)
    this.logger.debug(`Running retrieval for domain=${domain}`);
    const queryText = patient.symptoms ?? JSON.stringify(patient);
    const retrieved = await this.mlService.retrieveText(queryText, k);

    // ---------------------------------------------------------
    // FIX STARTS HERE
    // ---------------------------------------------------------
    
    // 2) Format data to match Python's PatientInput schema { age: int, symptoms: List[str] }
    
    // Convert symptoms to comma-separated string for Python API
    let symptomsStr: string = "";
    if (typeof patient.symptoms === 'string') {
      symptomsStr = patient.symptoms;
    } else if (Array.isArray(patient.symptoms)) {
      symptomsStr = patient.symptoms.join(", "); // Join array to string
    } else {
      symptomsStr = "Unknown symptoms"; // Fallback
    }

    // Ensure age is present and is a number
    const patientAge = patient.age ? parseInt(patient.age, 10) : 0;

    const payload = {
      age: patientAge,
      symptoms: symptomsStr  // Send as string (Python will handle it)
      // Note: We do NOT send 'retrieved' here because Python's PatientInput schema 
      // doesn't accept it, and your Python code runs rag_query() again anyway.
    };

    // 3) Call diagnose endpoint
    this.logger.debug('Calling ML diagnose endpoint');
    const mlResponse = await this.mlService.sendDiagnosisRequest(domain, payload);

    // ---------------------------------------------------------
    // FIX ENDS HERE
    // ---------------------------------------------------------

    // 4) Normalize/return
    return {
      domain,
      retrieved: mlResponse.retrieved ?? retrieved?.docs ?? retrieved,
      diagnosis: mlResponse.diagnosis,
      recommendation: mlResponse.rationale,
      confidence: mlResponse.confidence,
      scores: mlResponse.scores,
    };
  }
}



