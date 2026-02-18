FROM python:3.14-alpine

WORKDIR /ml

# Копируем и устанавливаем зависимости
COPY ../shared_config /ml/shared_config
COPY ml/requirements.txt /ml
RUN pip install -r requirements.txt

# Копируем код
COPY /ml /ml

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "ml", "--port", "8000"]