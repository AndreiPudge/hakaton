#!/bin/bash

# run.sh

# Активировать виртуальное окружение
source /Users/yurchenkonikita/hakaton/venv/bin/activate

# Генерируем API-ключ
python3 shared/generate_key.py

# Загружаем переменную в окружение
export $(grep -v '^#' .env | xargs)

# Запуск серверов в фоне
python3 -m uvicorn ml.app.main:app --host 0.0.0.0 --port 8000 &
SERVICE_PID=$!

python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 9000 &
BACKEND_PID=$!

echo "Сервер 1 запущен на порту 8000 (PID: $SERVICE_PID)"
echo "Сервер 2 запущен на порту 9000 (PID: $BACKEND_PID)"
echo "Для остановки нажмите Ctrl+C"

# Ждем прерывания и убиваем процессы
trap "kill $SERVICE_PID $BACKEND_PID 2>/dev/null; exit" INT TERM
#lsof -ti :8000 | xargs kill -9 
#lsof -ti :8000 | xargs kill -9 
wait