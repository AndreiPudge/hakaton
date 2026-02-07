import pandas as pd
import os
from pydantic import BaseModel
import random
from typing import List
from ml.app.config.config import settings as s

# Модель ответа
class ClientResponse(BaseModel):
    id: int
    gender: str
    city: str
    avg_spending_90_days: float

# Загружаем данные при старте

df = pd.read_csv(s.csv_data_path, sep=';')

# Преобразуем числовые колонки из строк с запятыми в float
df['avg_amount_daily_transactions_90d'] = (
    df['avg_amount_daily_transactions_90d']
    .astype(str)
    .str.replace(',', '.')
    .replace('nan', '0')
    .astype(float)
    .fillna(0)
)

def get_random_clients() -> List[ClientResponse]:
    #Возвращает случайные последовательные строки с нужными колонками
    count = 20

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