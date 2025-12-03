// import { Controller, Post, Body } from '@nestjs/common';
// import { MlGatewayService } from './ml.service';

// @Controller('api/ml')
// export class MlGatewayController {
//   constructor(private readonly ml: MlGatewayService) {}

//   @Post('retrieve')
//   async retrieve(@Body() body: { text: string; k?: number }) {
//     const { text, k } = body;
//     return this.ml.retrieve(text, k ?? 5);
//   }

//   @Post('diagnose')
//   async diagnose(@Body() patientDto: any) {
//     return this.ml.diagnose(patientDto);
//   }
// }


import { Controller, Post, Body, HttpException, HttpStatus, Param } from '@nestjs/common';
import { MlGatewayService } from './ml.service';

@Controller('ml')
export class MlGatewayController {
  constructor(private readonly mlService: MlGatewayService) {}
  // @Post('diagnose/:domain')
  // async diagnosePatient(@Body() patientData: any, @Param('domain') domain: string) {
  //   try {
  //     return await this.mlService.sendDiagnosisRequest(patientData, domain);
  //   } catch (e) {
  //     throw new HttpException(e.message, HttpStatus.BAD_GATEWAY);
  //   }
  // }

  @Post('retrieve')
  async retrieve(@Body() body: { text: string; k?: number }) {
    try {
      return await this.mlService.retrieveText(body.text, body.k ?? 3);
    } catch (e) {
      throw new HttpException(e.message, HttpStatus.BAD_GATEWAY);
    }
  }
}
