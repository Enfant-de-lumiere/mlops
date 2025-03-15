from http.client import HTTPException
from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
import datetime
import jwt
import uvicorn

# Connexion à MongoDB
MONGO_URL = "mongodb://mongodb:8080/"
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)  # Timeout après 3s
    db = client["test"]
    collection = db["test_collection"]
    users = db["users"]
    print("✅ Connexion réussie !")
    print("📌 Bases de données disponibles :", client.list_database_names())
    print("Collection", collection)
    print("DB", db)
except Exception as e:
    print("❌ Erreur de connexion :", e)

app = FastAPI()
#Récuperer les documents
@app.get("/data")
async def get_data():
    return [{"_id": str(doc["_id"]), "value": doc["value"]} for doc in collection.find()]

# Récupérer un document par ID
@app.get("/data/{doc_id}")
async def get_data_by_id(doc_id: str):
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    return {"_id": str(doc["_id"]), "value": doc["value"]} if doc else {"error": "Document non trouvé"}

# Ajouter un document
@app.post("/data")
async def add_data(data: dict):
    result = collection.insert_one(data)
    return {"_id": str(result.inserted_id)}

# Supprimer un document
@app.delete("/data/{doc_id}")
async def delete_data(doc_id: str):
    result = collection.delete_one({"_id": ObjectId(doc_id)})
    return {"deleted": result.deleted_count > 0}

def create_jwt(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire dans 1h
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# 📌 Fonction d'authentification
@app.post("/authenticate")
async def authenticate(data: dict):
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username, "password": password})

    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    role = user.get("role", "USER")

    token = create_jwt(username, role)

    return {"access_token": token, "token_type": "bearer", "role": role}


