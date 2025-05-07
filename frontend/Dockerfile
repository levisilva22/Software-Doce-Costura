FROM node:20-alpine as build
WORKDIR /app

# Copie apenas os arquivos de dependências primeiro
COPY package*.json ./
RUN npm install

# Depois copie o restante dos arquivos
COPY public ./public
COPY src ./src
COPY .env* ./

# Construa o aplicativo
RUN npm run build

# Imagem de produção
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]