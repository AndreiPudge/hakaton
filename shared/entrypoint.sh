#!/bin/bash

# Генерация таблицы
python3 ml_functions/db/init_db.py
python3 ml_functions/db/paste_insights.py