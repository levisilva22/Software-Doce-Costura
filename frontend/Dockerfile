FROM node:20-alpine as build

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração de pacotes
COPY package.json package-lock.json ./

# Instala as dependências
RUN npm ci --silent

# Copia o código fonte
COPY . .

# Define as variáveis de ambiente para a build
ARG REACT_APP_API_URL=http://localhost:8000/api
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Gera a build de produção
RUN npm run build

# Estágio 2: Servidor Nginx para servir o frontend
FROM nginx:alpine

# Copia os arquivos estáticos da build
COPY --from=build /app/build /usr/share/nginx/html

# Copia a configuração personalizada do Nginx (se necessária)
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

RUN pip install --no-cache-dir -r requirements.txt
# Expõe a porta 80
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]