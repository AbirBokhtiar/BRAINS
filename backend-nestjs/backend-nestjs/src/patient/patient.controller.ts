import { Controller, Get } from '@nestjs/common';
import { PatientService } from './patient.service';

@Controller('patient')
export class PatientController {
  constructor(private readonly service: PatientService) {}

  @Get()
  getAll() {
    return this.service.getPatients();
  }
}
