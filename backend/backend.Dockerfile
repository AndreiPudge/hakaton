FROM python:3.14-alpine

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY /backend ./

ENV PYTHONUNBUFFERED=1

CMD ["python3", "-u", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8443"]