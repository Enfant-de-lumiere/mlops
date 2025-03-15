from typing import Optional
from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
from bson import ObjectId
import datetime
import jwt

# Connexion à MongoDB
MONGO_URL = "mongodb://mongodb:27017/"
SECRET_KEY = "secretKey"
ALGORITHM = "HS256"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)  # Timeout après 3s
    db = client["test"]
    collection = db["test_collection"]
    users = db["users"]
    print("Connexion réussie !")
    print("Bases de données disponibles :", client.list_database_names())
    print("Collection", collection)
    print("DB", db)
except Exception as e:
    print("Erreur de connexion :", e)



security = HTTPBearer()
app = FastAPI()

# Autoriser CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def get_current_user(token: str) -> Optional[dict]:
    """Décode le token JWT et retourne les infos utilisateur (ou None si invalide)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "role": payload["role"]}
    except jwt.PyJWTError:
        return None
    
def token_valid(token: str, required_role: str = "ADMIN"):
    """Vérifie si le token est valide et si l'utilisateur a le bon rôle."""
    user = get_current_user(token)

    if not user:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    if user["role"] != required_role:
        raise HTTPException(status_code=403, detail=f"Seuls les utilisateurs ayant le role {required_role} peuvent effectuer cette action")


#Récuperer les documents
@app.get("/data")
async def get_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_valid(credentials.credentials)
    return [{"_id": str(doc["_id"]), "value": doc["value"]} for doc in collection.find()]

# Récupérer un document par ID
@app.get("/data/{doc_id}")
async def get_data_by_id(doc_id: str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_valid(credentials.credentials)
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    return {"_id": str(doc["_id"]), "value": doc["value"]} if doc else {"error": "Document non trouvé"}

# Ajouter un document
@app.post("/data")
async def add_data(data: dict,credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    
    result = collection.insert_one(data)
    return {"_id": str(result.inserted_id)}

# Mettre à jour un document
@app.put("/data/{doc_id}")
async def update_data(doc_id: str, data: dict,credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_valid(credentials.credentials)
    result = collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": data}
    )
    return {"_id": doc_id}

# Supprimer un document
@app.delete("/data/{doc_id}")
async def delete_data(doc_id: str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_valid(credentials.credentials)
    result = collection.delete_one({"_id": ObjectId(doc_id)})
    return {"deleted": result.deleted_count > 0}

#Créer un token d'accès d'1 heure avec JWT
def create_jwt(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire dans 1h
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Authentifier l'utilisateur
@app.post("/authenticate")
async def authenticate(data: dict):
    """
    il regarde si il est présent dans la base,
    si c'est le cas renvoit un token d'accès d'1 heure,
    sinon renvoit une erreur 401.
    """
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username, "password": password})

    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    role = user.get("role", "USER")

    token = create_jwt(username, role)

    return {"access_token": token, "token_type": "bearer", "role": role}


