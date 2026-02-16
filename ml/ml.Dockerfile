FROM python:3.14-slim

WORKDIR /ml

# Копируем и устанавливаем зависимости
COPY ml/requirements.txt /ml
RUN pip install -r requirements.txt

# Копируем код
COPY /ml /ml

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]