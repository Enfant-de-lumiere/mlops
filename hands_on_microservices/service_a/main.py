from fastapi import FastAPI
import httpx


URL = "http://service_b"

# Define the path to the Unix Domain Socket
uds_path = "/tmp/service_b.sock"
# Use a custom transport to make requests via the UDS
transport = httpx.AsyncHTTPTransport(uds=uds_path)

app = FastAPI()

token= ""

@app.get("/data")
async def get_data():
    url = f"{URL}/data"
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(url)
    return response.json()


# Récupérer un document par ID
@app.get("/data/{doc_id}")
async def get_data_by_id(doc_id: str):
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(f"{URL}/data/{doc_id}")
        return response.json()

# Ajouter un document
@app.post("/post_data")
async def add_data(name: str, value: int):
    async with httpx.AsyncClient(transport=transport) as client:
        data = {"value": value}
        response = await client.post(f"{URL}/data", json=data)
        return response.json()

# Supprimer un document
@app.delete("/data/{doc_id}")
async def delete_data(doc_id: str):
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.delete(f"{URL}/data/{doc_id}")
        return response.json()
    
@app.post("/authenticate")
async def authenticate(username: str, password: str):
    async with httpx.AsyncClient(transport=transport) as client:
        data = {"username": username, "password": password}
        response = await client.post(f"{URL}/authenticate", json=data)
        token = response.json()
        return response.json()