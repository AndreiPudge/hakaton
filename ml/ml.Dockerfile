FROM python:3.14-alpine

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY ../shared_config ./shared_config

COPY ml/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY /ml ./

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "ml", "--port", "8000"]