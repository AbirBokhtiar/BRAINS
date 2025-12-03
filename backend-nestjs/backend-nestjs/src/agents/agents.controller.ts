import { Body, Controller, Post } from '@nestjs/common';
import { AgentsService } from './agents.service';

class AgentRequest {
  domain: 'cardiology' | 'neurology' | 'pulmonology' | 'general';
  patient: any;
  k?: number;
}

@Controller('agents')
export class AgentsController {
  constructor(private readonly svc: AgentsService) {}

  @Post('run')
  async run(@Body() body: AgentRequest) {
    const { domain, patient, k = 5 } = body;
    return this.svc.runAgent(domain, patient, k);
  }
}
