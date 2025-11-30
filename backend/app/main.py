from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.endpoints import ml, data, buttons
from pydantic import BaseModel
import os
import uvicorn
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ml.router, prefix="/api/ml", tags=["ml"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(buttons.router, prefix="/api/buttons", tags=["buttons"])

# URL ML-сервиса из переменных окружения
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8000")

# Глобальная переменная для хранения данных
ml_data_cache = None

# Добавь эту модель
class PredictRequest(BaseModel):
    id: int

@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is running"}

# Функция для получения данных из ML-сервиса при старте
@app.on_event("startup")
async def startup_event():
    await fetch_ml_data()

# Функция для связи с ML-сервисом
async def fetch_ml_data():
    global ml_data_cache
    try:
        response = requests.get(
            f"{ML_SERVICE_URL}/random-clients",
            timeout=30
        )
        response.raise_for_status()
        ml_data_cache = response.json()
        print(f"Loaded {len(ml_data_cache)} clients from ML service")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from ML service: {e}")
        ml_data_cache = []

# Эндпоинт для получения данных (будет использоваться фронтом)
@app.get("/api/ml/clients")
async def get_ml_clients():
    if ml_data_cache is None:
        await fetch_ml_data()
    
    if not ml_data_cache:
        raise HTTPException(status_code=500, detail="No data available from ML service")
    
    return ml_data_cache

@app.post("/api/ml/predict")
async def predict_client(request: PredictRequest):
    """Получает ID от фронта, отправляет в ML-сервис, возвращает предсказание"""
    try:
        # Отправляем ID в ML-сервис
        response = requests.post(
            f"{ML_SERVICE_URL}/predict",
            json={"id": request.id},
            timeout=30
        )
        response.raise_for_status()
        
        # Возвращаем предсказание фронту
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"ML service error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    uvicorn.run(app, host="0.0.0.0", port=port)
