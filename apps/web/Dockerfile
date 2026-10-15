FROM node:22-slim

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3005

CMD ["npm", "run", "start", "--", "--port", "3005"]
