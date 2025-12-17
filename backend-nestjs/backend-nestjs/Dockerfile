# backend-nestjs/Dockerfile
# FROM node:20-alpine
# WORKDIR /app
# COPY package*.json ./
# RUN npm ci
# COPY . .
# RUN npm run build
# ENV NODE_ENV=production
# EXPOSE 4000
# CMD ["node", "dist/main.js"]
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# VERY IMPORTANT
RUN npm ci --omit=dev

COPY . .

RUN npm run build

EXPOSE 4000

CMD ["node", "dist/main.js"]
ENV NODE_ENV=production