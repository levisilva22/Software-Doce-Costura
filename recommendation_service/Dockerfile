FROM python:3.10-slim

WORKDIR /recommendation_service

# Configurações Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Configurações Django
ENV DJANGO_SETTINGS_MODULE=recommendation_service.settings
ENV DEBUG=False
ENV SECRET_KEY=change_this_in_production
ENV ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações de Banco de Dados
ENV DB_ENGINE=django.db.backends.postgresql
ENV DB_NAME=recommendation_db
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=recommendation_db
ENV DB_PORT=5432


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0:8000"]  

