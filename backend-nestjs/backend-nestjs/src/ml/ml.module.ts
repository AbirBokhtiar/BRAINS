import { Module } from '@nestjs/common';
import { MlGatewayService } from './ml.service';
import { MlGatewayController } from './ml.controller';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [HttpModule],
  controllers: [MlGatewayController],
  providers: [MlGatewayService],
  exports: [MlGatewayService],
})
export class MlGatewayModule {}
