# Stage 1: Build
FROM node:18-alpine as build

WORKDIR /app

# Argumento para la URL del API
ARG REACT_APP_API_URL=/api/
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Copiar package.json e instalar dependencias
COPY package.json package-lock.json* ./
RUN npm install

# Copiar codigo fuente y construir
COPY . .
RUN npm run build

# Stage 2: Servir con Nginx
FROM nginx:alpine

# Copiar build de React
COPY --from=build /app/build /usr/share/nginx/html

# Copiar configuracion de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
