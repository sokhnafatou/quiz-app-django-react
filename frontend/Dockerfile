# Image du frontend React (Vite).
# Build multi-stage : on compile les assets puis on sert avec nginx.

# --- Étape 1 : build ---
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
# L'URL de l'API est injectée à la compilation via VITE_API_URL.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- Étape 2 : serveur statique ---
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
