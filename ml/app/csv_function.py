import csv
import random
from pathlib import Path
from pydantic import BaseModel
from typing import List
from shared_config.config import settings as s

BASE_DIR = Path(__file__).resolve().parent.parent.parent
csv_path = BASE_DIR / s.csv_data_path

class ClientResponse(BaseModel):
    id: int
    gender: str
    city: str
    avg_spending_90_days: float

# Загружаем данные в список словарей
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    df = []
    for row in reader:
        row['avg_amount_daily_transactions_90d'] = float(
            row['avg_amount_daily_transactions_90d'].replace(',', '.') or 0
        )
        row['id'] = int(row['id'])
        df.append(row)

def get_random_clients() -> List[ClientResponse]:
    count = 20
    if count > len(df):
        count = len(df)
    
    start_idx = random.randint(0, len(df) - count)
    random_data = df[start_idx:start_idx + count]

    clients = [
        ClientResponse(
            id=row['id'],
            gender=row['gender'],
            city=row['city_smart_name'],
            avg_spending_90_days=row['avg_amount_daily_transactions_90d']
        )
        for row in random_data
    ]
    return clients
