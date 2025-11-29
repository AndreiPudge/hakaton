# backend build
FROM python:3.9-alpine

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

ENV PORT=9000

EXPOSE 9000

# Запускаем приложение
CMD ["python3", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]