import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { json } from 'express';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    cors: true,
  });
  app.use(json({ limit: '2mb' }));
  await app.listen(process.env.PORT ? parseInt(process.env.PORT) : 4000);
  console.log('Backend NestJS listening on port', process.env.PORT || 4000);
}
bootstrap();

// async function bootstrap() {
//   const app = await NestFactory.create(AppModule);
//   await app.listen(process.env.PORT ?? 3000);
// }

// import { ValidationPipe } from '@nestjs/common';
// import { NestFactory } from '@nestjs/core';
// import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
// import { AppModule } from './app.module';

// async function bootstrap() {
//   const app = await NestFactory.create(AppModule);

//   // Global validation
//   app.useGlobalPipes(
//     new ValidationPipe({
//       whitelist: true,
//       forbidNonWhitelisted: false,
//       transform: true,
//     }),
//   );

//   // Swagger
//   const config = new DocumentBuilder()
//     .setTitle('BRAINS Backend')
//     .setDescription('NestJS backend for the BRAINS multi-agent diagnostic platform')
//     .setVersion('1.0')
//     .addTag('ml', 'ML proxy endpoints')
//     .addTag('patient', 'Patient CRUD')
//     .build();
//   const doc = SwaggerModule.createDocument(app, config);
//   SwaggerModule.setup('docs', app, doc);

//   const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
//   await app.listen(port);
//   console.log(`Server listening on http://localhost:${port}`);
// }
// bootstrap();
