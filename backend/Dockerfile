# Image du backend Django + DRF.
# Multi-stage léger : on installe les dépendances puis on lance gunicorn.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dépendances système minimales pour psycopg2.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Script de démarrage : migrations + données d'exemple + serveur.
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "quiz_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
