import { Test, TestingModule } from '@nestjs/testing';
import { MlGatewayService } from './ml.service';

describe('MlService', () => {
  let service: MlGatewayService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [MlGatewayService],
    }).compile();

    service = module.get<MlGatewayService>(MlGatewayService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
