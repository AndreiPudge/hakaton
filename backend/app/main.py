from fastapi import FastAPI, Request
import httpx
import time
from contextlib import asynccontextmanager
from backend.app.api.router import router
from fastapi.middleware.cors import CORSMiddleware
import os
from backend.app.config.config import settings as s
from backend.app.middleware.hmr_filter import hmr_filter_middleware
from asyncio import Semaphore
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(wait_for_service())
    yield

app = FastAPI(lifespan=lifespan, title = "Backen API")

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
    print("WARNING:     SERVICE_API_KEY NOT SET!")
service_client = httpx.AsyncClient(
    base_url=f"{s.domain}:{s.service_port}",
    headers={"X-API-KEY": SERVICE_KEY} if SERVICE_KEY else {}
)

#######################################################

### SERVICE CONNECTION CHECK ###

async def wait_for_service(url: str = f"{s.domain}:{s.service_port}/health", timeout: int = 30):
    async with httpx.AsyncClient() as client:
        for i in range(timeout):
            try:
                response = await client.get(url, timeout = 1)
                if response.status_code == 200:
                    return
            except:
                time.sleep(1)
        print(f"INFO:     {s.domain}:{s.service_port} - Timeout ERROR!")

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
        timeout = httpx.Timeout(30.0, connect=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
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
