#!/bin/bash

# run.sh

# Активировать виртуальное окружение
source /Users/yurchenkonikita/hakaton/venv/bin/activate

# Генерируем API-ключ
python3 shared/generate_key.py

# Загружаем переменную в окружение
export $(grep -v '^#' .env | xargs)
export $(grep -v '^#' shared/.env.keys | xargs)

# Логи
LOG_FILE="../console.log"
> "$LOG_FILE"

cd ml
# Запуск серверов в фоне
python3 -m uvicorn app.main:app --host $SERVICE_HOST --port $SERVICE_PORT 2>&1 | tee -a "$LOG_FILE" &
#python3 -m uvicorn ml.app.main:app --host $SERVICE_HOST --port $SERVICE_PORT --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem &
SERVICE_PID=$!
cd ..

cd backend
python3 -m uvicorn app.main:app --host $BACKEND_HOST --port $BACKEND_PORT 2>&1 | tee -a "$LOG_FILE" &
#python3 -m uvicorn backend.app.main:app --host $BACKEND_HOST --port $BACKEND_PORT --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem &
BACKEND_PID=$!
cd ..

sleep 5

echo "Сервис запущен на порту $SERVICE_PORT (PID: $((SERVICE_PID-1)))" | tee -a "$LOG_FILE"
echo "Бекенд запущен на порту $BACKEND_PORT (PID: $((BACKEND_PID-1)))" | tee -a "$LOG_FILE"

cd frontend

npm start 2>&1 | tee -a "../$LOG_FILE" &
FRONTEND_PID=$!

echo "Фронтенд запущен на порту $FRONTEND_PORT (PID: $FRONTEND_PID)"
echo "Для остановки нажмите Ctrl+C" 

# Ждем прерывания и убиваем процессы
trap "kill $SERVICE_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM | tee -a "$LOG_FILE"
#lsof -ti :$SERVICE_PORT | xargs kill -9 
#lsof -ti :$BACKEND_PORT | xargs kill -9 
wait