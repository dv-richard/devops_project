# Étape 1 : image de base Python
FROM python:3.10-slim

# Étape 2 : répertoire de l'application
WORKDIR /app

# Étape 3 : copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Étape 4 : point d'entrée (à adapter selon ton app)
CMD CMD ["uvicorn", "hexencoder:app", "--host", "0.0.0.0", "--port", "5000"]
