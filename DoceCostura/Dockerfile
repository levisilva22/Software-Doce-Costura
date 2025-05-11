FROM python:3.10-slim

# Configurar diretório de trabalho
WORKDIR /app

# Configurações Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Configurações Django
ENV DJANGO_SETTINGS_MODULE=DoceCostura.settings
ENV DEBUG=False
ENV SECRET_KEY=${MAIN_SECRET_KEY}
ENV ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações de Banco de Dados
ENV DB_ENGINE=django.db.backends.postgresql
ENV DB_NAME=docecostura_db
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=docecostura_db
ENV DB_PORT=5432

# Configurações dos gateways de pagamento
ENV STRIPE_PUBLIC_KEY=${STRIPE_PUBLIC_KEY}
ENV STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
ENV STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
ENV MERCADOPAGO_PUBLIC_KEY=${MERCADOPAGO_PUBLIC_KEY}
ENV MERCADOPAGO_ACCESS_TOKEN=${MERCADOPAGO_ACCESS_TOKEN}
ENV PAGHIPER_API_KEY=${PAGHIPER_API_KEY}
ENV PAGHIPER_TOKEN=${PAGHIPER_TOKEN}

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Porta que o servidor vai escutar
EXPOSE 8000

# Configurar volume para mídia e arquivos estáticos
VOLUME ["/DoceCostura/media", "/DoceCostura/static"]


# Iniciar com o script de inicialização
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]