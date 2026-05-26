# Stage 1 — Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build -- --configuration=production

# Stage 2 — Runtime Nginx
FROM nginx:alpine AS runtime

# Copier le build Angular
COPY --from=builder /app/dist/frontend/browser \
  /usr/share/nginx/html

# Configuration Nginx sécurisée
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -qO- http://localhost/health || exit 1
