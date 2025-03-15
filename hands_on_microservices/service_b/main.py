from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

# Connexion à MongoDB
MONGO_URL = "mongodb://mongodb:8001/"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)  # Timeout après 3s
    db = client["test"]
    collection = db["test_collection"]
    print("Connexion réussie !")
    print("Bases de données disponibles :", client.list_database_names())
    print("Collection", collection)
    print("DB", db)
except Exception as e:
    print("Erreur de connexion :", e)

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



