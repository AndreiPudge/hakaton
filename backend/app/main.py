from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
import time
from backend.app.api.router import router
from fastapi.middleware.cors import CORSMiddleware
import os
from config.config import settings as s


### Server Launching ###
def wait_for_service(url: str = f"{s.domain}:{s.backend_port}/health", timeout: int = 30):
    # Ожидание ответа сервиса
    for i in range(timeout):
        try:
            response = httpx.get(url, verify=False, timeout = 1)
            if response.status_code == 200:
                return
        except:
            time.sleep(1)
    raise TimeoutError(f"Service ERROR! ({url})")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Waiting for service on port {s.service_port}...")
    wait_for_service(f"{s.domain}:{s.service_port}/health")
    print(f"Service on port {s.service_port} is ready!")
    yield
    print("Server shutdown.")

app = FastAPI(lifespan=lifespan, title="Backend API")

#######################################################

### CORS ###

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#######################################################

### Client Modifications ###

SERVICE_KEY = os.getenv("SERVICE_API_KEY")
if not SERVICE_KEY:
    raise RuntimeError("SERVICE_API_KEY not set")
service_client = httpx.AsyncClient(
    base_url=f"{s.domain}:{s.service_port}",
    headers={"X-API-KEY": SERVICE_KEY}
)

#######################################################

### Endpoints ###

app.include_router(router)

# Service Predict
@app.post("/api/predict")
async def api_prediction():
    async with httpx.AsyncClient() as client:
        response = await service_client.post(f"{s.domain}:{s.service_port}/predict")
        return response.json

# Service Random Clients
@app.post("/api/random-cli")
async def api_random_clients():
    async with httpx.AsyncClient() as client:
        response = await service_client.post(f"{s.domain}:{s.service_port}/random-cli")
        return response.json

# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}

# Backend API
@app.get("/")
def backapi():
    return "Backend API!"

#######################################################
