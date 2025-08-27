# Utilisation de l'image Python officielle
FROM python:3.13-slim

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.8.0+cpu --index-url https://download.pytorch.org/whl/cpu

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code de l'application
COPY main.py .
COPY static/ ./static/

# Exposition du port 7860 (requis pour Hugging Face Spaces)
EXPOSE 7860

# Variables d'environnement
ENV PYTHONPATH=/app
ENV TRANSFORMERS_CACHE=/app/cache

# Création du répertoire de cache
RUN mkdir -p /app/cache

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]