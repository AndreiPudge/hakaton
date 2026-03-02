from fastapi import FastAPI, Request
import httpx
import time
from contextlib import asynccontextmanager
from app.api.router import router
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.settings import settings as s
from app.middleware.hmr_filter import hmr_filter_middleware
from asyncio import Semaphore
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="INFO:     %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("adasd")
    asyncio.create_task(wait_for_service())
    yield

app = FastAPI(lifespan=lifespan, title = "Backen API")

#######################################################

### CORS ###

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{s.frontend_host}:{s.frontend_port}"],
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

### SERVICE CONNECTION CHECK ###

async def wait_for_service(url: str = f"http://{s.service_host}:{s.service_port}/health", timeout: int = 30):
    async with httpx.AsyncClient() as client:
        for i in range(timeout):
            try:
                response = await client.get(url, timeout = 1)
                if response.status_code == 200:
                    return logger.info(f"Connection to the Service on port [{s.service_port}] is established!")
            except:
                time.sleep(1)
        logger.info(f"{s.service_host}:{s.service_port} - Timeout ERROR!")

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
            response = await client.post(f"http://{s.service_host}:{s.service_port}/clients/{client_id}/insights")
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
        response = await client.post(f"http://{s.service_host}:{s.service_port}/random-cli")
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
