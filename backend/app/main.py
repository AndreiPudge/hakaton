from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import httpx
import time
from backend.app.api.router import router
from fastapi.middleware.cors import CORSMiddleware
import os
from backend.app.config.config import settings as s
from backend.app.middleware.hmr_filter import hmr_filter_middleware
from asyncio import Semaphore
import asyncio


### Server Launching ###
def wait_for_service(url: str = f"{s.domain}:{s.service_port}/health", timeout: int = 30):
    # Ожидание ответа сервиса
    for i in range(timeout):
        try:
            response = httpx.get(url, timeout = 1)
            if response.status_code == 200:
                return
        except:
            time.sleep(1)
    raise TimeoutError(f"Service ERROR! ({url})")

@asynccontextmanager
async def lifespan(app: FastAPI):
    #print(f"Waiting for service on port {s.service_port}...")
    wait_for_service(f"{s.domain}:{s.service_port}/health")
    #print(f"Service on port {s.service_port} is ready!")
    #print(f"Starting server on port {s.backend_port}...")
    yield
    #print("Server shutdown.")

app = FastAPI(lifespan=lifespan, title="Backend API")

#######################################################

### CORS ###

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"{s.domain}:{s.frontend_port}"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#######################################################

### MIDDLEWARE ###

@app.middleware("http")
async def hmr_middleware(request: Request, call_next):
    return await hmr_filter_middleware(request, call_next)

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

### QUEUE and CACHE ###

# Prediction (insights)
ml_semaphore = Semaphore(1)
prediction_cache = {}
CACHE_TTL=300 # 5 minutes

#######################################################

### Endpoints ###

app.include_router(router)

# Service Predict
@app.post("/api/clients/{client_id}/insights")
async def api_prediction(client_id: int):
    # CACHE check
    if client_id in prediction_cache:
        return prediction_cache[client_id]
    
    # SEMAPHORE QUEUE
    async with ml_semaphore:
        async with httpx.AsyncClient(timeout = 30.0) as client:
            response = await service_client.post(f"{s.domain}:{s.service_port}/clients/{client_id}/insights")
            result = response.json()

            # CACHE SAVE
            prediction_cache[client_id] = result

            # Auto-clear cache after TTL
            async def clear_single_cache():
                await asyncio.sleep(CACHE_TTL)
                prediction_cache.pop(client_id, None)
            
            asyncio.create_task(clear_single_cache())
            
            return result

# Service Random Clients
@app.post("/api/random-cli")
async def api_random_clients():
    async with httpx.AsyncClient() as client:
        response = await service_client.post(f"{s.domain}:{s.service_port}/random-cli")
        return response.json()

# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}

# Backend API
@app.get("/")
def backapi():
    return "Backend API!"

#######################################################
