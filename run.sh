#!/bin/bash

# run.sh

# Активировать виртуальное окружение
source /Users/yurchenkonikita/hakaton/venv/bin/activate

# Генерируем API-ключ
python3 shared/generate_key.py

# Загружаем переменную в окружение
export $(grep -v '^#' config/.env | xargs)
export $(grep -v '^#' shared/.env.keys | xargs)

# Запуск серверов в фоне
python3 -m uvicorn ml.app.main:app --host $SERVICE_HOST --port $SERVICE_PORT &
#python3 -m uvicorn ml.app.main:app --host $SERVICE_HOST --port $SERVICE_PORT --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem &
SERVICE_PID=$!

python3 -m uvicorn backend.app.main:app --host $BACKEND_HOST --port $BACKEND_PORT &
#python3 -m uvicorn backend.app.main:app --host $BACKEND_HOST --port $BACKEND_PORT --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem &
BACKEND_PID=$!

echo "Сервер 1 запущен на порту $SERVICE_PORT (PID: $SERVICE_PID)"
echo "Сервер 2 запущен на порту $BACKEND_PORT (PID: $BACKEND_PID)"
echo "Для остановки нажмите Ctrl+C"

# Ждем прерывания и убиваем процессы
trap "kill $SERVICE_PID $BACKEND_PID 2>/dev/null; exit" INT TERM
#lsof -ti :$SERVICE_PORT | xargs kill -9 
#lsof -ti :$BACKEND_PORT | xargs kill -9 
wait