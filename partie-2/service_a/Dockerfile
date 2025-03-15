FROM python:3.11-slim

# Installer Flask et ses dépendances
RUN pip install flask flask-cors requests

COPY main.py /app/main.py
COPY templates /app/templates

WORKDIR /app

# Définir les variables d'environnement pour Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=1 

EXPOSE 8000
# Commande pour lancer Flask
CMD ["flask", "run"]
