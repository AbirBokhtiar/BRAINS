import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AuthModule } from './patient/auth/auth.module';
import { PatientController } from './patient/patient.controller';
import { MlGatewayService } from './ml/ml.service';
import { HttpModule } from '@nestjs/axios';
import { ConfigModule } from '@nestjs/config';
import { MlGatewayModule } from './ml/ml.module';
import { AgentsModule } from './agents/agents.module';
import { MlGatewayController } from './ml/ml.controller';
import { AgentsController } from './agents/agents.controller';
import { AgentsService } from './agents/agents.service';
import { PatientService } from './patient/patient.service';

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), HttpModule.register({ timeout: 10000 }), MlGatewayModule, AuthModule, AgentsModule],
  controllers: [AppController, PatientController, MlGatewayController, AgentsController],
  providers: [AppService, PatientService, MlGatewayService, AgentsService],
})
export class AppModule {}
