FROM python:3.14-alpine

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY ../shared_config ./shared_config

COPY backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY /backend ./

EXPOSE 9000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "backend", "--port", "9000"]