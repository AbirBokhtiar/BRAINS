// // ml-gateway.service.ts
// import { Injectable } from '@nestjs/common';
// import { HttpService } from '@nestjs/axios';
// import { lastValueFrom } from 'rxjs';

// @Injectable()
// export class MlGatewayService {
//   constructor(private readonly httpService: HttpService) {}

//   private mlUrl(): string {
//     return process.env.ML_SERVICE_URL || 'http://127.0.0.1:8000';
//   }

//   // Simple safety check
//   private safetyFilter(text: string): { ok: boolean; reason?: string } {
//     // very small sample set — expand for production
//     const blockedKeywords = ['suicide', 'self-harm', 'dose', 'dosage', 'take', 'kill'];
//     const lower = text.toLowerCase();
//     for (const k of blockedKeywords) {
//       if (lower.includes(k)) return { ok: false, reason: `Contains blocked keyword: ${k}` };
//     }
//     return { ok: true };
//   }

//   async retrieve(text: string, k = 5) {
//     // run safety filter
//     const sf = this.safetyFilter(text);
//     if (!sf.ok) {
//       return { error: 'input blocked for safety', reason: sf.reason };
//     }
//     const url = `${this.mlUrl()}/api/retrieve`;
//     const resp$ = this.httpService.post(url, { text, k });
//     const resp = await lastValueFrom(resp$);
//     return resp.data;
//   }

//   async diagnose(patientDto: any) {
//     // basic stringify check for safety
//     const summary = JSON.stringify(patientDto).slice(0, 1000);
//     const sf = this.safetyFilter(summary);
//     if (!sf.ok) return { error: 'input blocked for safety', reason: sf.reason };
//     const url = `${this.mlUrl()}/api/ml/diagnose`;
//     const resp$ = this.httpService.post(url, patientDto);
//     const resp = await lastValueFrom(resp$);
//     return resp.data;
//   }
// }

import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class MlGatewayService {
  private ML_BASE = process.env.ML_SERVICE_URL || 'http://localhost:8000';

  async sendDiagnosisRequest(domain: string, patientData: any) {
    const url = `${this.ML_BASE}/api/ml/diagnose/${domain}`;

    const response = await axios.post(url, patientData, {
      timeout: 15000,
    });

    return response.data;
  }

  async retrieveText(text: string, k: number) {
    const url = `${this.ML_BASE}/api/retrieve`;

    const response = await axios.post(url, { text, k }, {
      timeout: 10000,
    });

    return response.data;
  }
}

