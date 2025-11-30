from fastapi import FastAPI, HTTPException
import pandas as pd
import random
from pydantic import BaseModel
from typing import List
import os
from ml.app.predict_function import predict

app = FastAPI()

# Загружаем данные при старте
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
csv_path = os.path.join(data_dir, 'hackathon_income_test.csv')  # Полный путь к файлу
df = pd.read_csv(csv_path, sep=';')

# Преобразуем числовые колонки из строк с запятыми в float
df['avg_amount_daily_transactions_90d'] = (
    df['avg_amount_daily_transactions_90d']
    .astype(str)
    .str.replace(',', '.')
    .replace('nan', '0')
    .astype(float)
    .fillna(0)
)

class ClientResponse(BaseModel):
    id: int
    gender: str
    city: str
    avg_spending_90_days: float

class PredictionRequest(BaseModel):  # Добавь эту модель
    id: int

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/random-clients")
async def get_random_clients() -> List[ClientResponse]:
    #Возвращает случайные последовательные строки с нужными колонками
    count = 100

    if count > len(df):
        count = len(df)
    
    # Выбираем случайные последовательные строки
    start_idx = random.randint(0, len(df) - count)
    random_data = df.iloc[start_idx:start_idx + count]
    
    # Преобразуем в ответ (замените названия колонок на актуальные из вашего файла)
    clients = []
    for _, row in random_data.iterrows():
        client = ClientResponse(
            id=int(row['id']),
            gender=str(row['gender']),
            city=str(row['city_smart_name']),
            avg_spending_90_days=float(row['avg_amount_daily_transactions_90d'])
        )
        clients.append(client)
    
    return clients

@app.post("/predict")
async def predict_single(request: PredictionRequest):
    # Находим запись по ID
    client_data = df[df['id'] == request.id].iloc[0:1]
    
    if client_data.empty:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Вызываем твою функцию predict
    prediction = predict(client_data)[0]
    
    return {"id": request.id, "prediction": float(prediction)}

