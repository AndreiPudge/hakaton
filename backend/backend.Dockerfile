FROM python:3.14-alpine

WORKDIR /backend

# Копируем и устанавливаем зависимости
COPY backend/requirements.txt /backend
RUN pip install -r requirements.txt

# Копируем код
COPY /backend /backend

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]