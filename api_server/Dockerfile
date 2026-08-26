FROM node:20-slim

WORKDIR /app

COPY api_server/package*.json ./
RUN npm install --omit=dev

COPY api_server/ .

EXPOSE 3333 8107

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD node -e "const http = require('http'); http.get('http://localhost:3333/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1)).on('error', () => process.exit(1));"

CMD ["node", "server.js"]