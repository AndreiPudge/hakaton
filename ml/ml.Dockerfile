FROM python:3.14-alpine

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY ml/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY /ml ./

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]