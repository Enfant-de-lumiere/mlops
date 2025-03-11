# Use a lightweight Python image
FROM python:3.11-slim

# Install FastAPI and Uvicorn and Pymongo
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/mongodb-server-keyring.gpg] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list && \
    apt-get update && apt-get install -y mongodb-mongosh && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install fastapi uvicorn pymongo
# # Copy the application code
COPY main.py /app/main.py
# Set the working directory to /app
WORKDIR /app
# Expose UDS path as a volume
VOLUME ["/tmp"]
# Run Uvicorn using the Unix Domain Socket
CMD ["uvicorn", "main:app", "--uds", "/tmp/service_b.sock", "--reload"]
