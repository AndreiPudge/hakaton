from fastapi import FastAPI
import pandas as pd
import random
from pydantic import BaseModel
from typing import List

app = FastAPI(title="ML Data Service")

# Загружаем данные при старте
df = pd.read_excel("data/123.xlsx")

class ClientResponse(BaseModel):
    id: int
    gender: str
    city: str
    avg_spending_90_days: float

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/random-clients/{count}")
async def get_random_clients(count: int = 100) -> List[ClientResponse]:
    """Возвращает случайные последовательные строки с нужными колонками"""
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
            city=str(row['city_smart_name']),  # замените на актуальное название
            avg_spending_90_days=float(row.get('summarur_1m_purch', 0))  # замените на актуальное
        )
        clients.append(client)
    
    return clients

@app.get("/client/{client_id}")
async def get_client_by_id(client_id: int) -> ClientResponse:
    """Получить конкретного клиента по ID"""
    client_data = df[df['id'] == client_id].iloc[0]
    
    return ClientResponse(
        id=int(client_data['id']),
        gender=str(client_data['gender']),
        city=str(client_data['city_smart_name']),
        avg_spending_90_days=float(client_data.get('summarur_1m_purch', 0))
    )