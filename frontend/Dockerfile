FROM node:20-alpine as build

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração de pacotes
COPY package.json package-lock.json ./


COPY . .

EXPOSE 3000

CMD ["npm", "start"]