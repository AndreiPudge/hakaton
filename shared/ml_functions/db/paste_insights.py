import sqlite3
import sys
from pathlib import Path

ml_function_path = Path("ml_functions").resolve()
sys.path.append(str(ml_function_path))

from predict_function import predict

database_path = Path("/data/insights.db")

def paste_insights_to_db():
    predictions = predict()

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for pred in predictions:
        cursor.execute('INSERT INTO insights (insight) VALUES (?)', (pred,))

    conn.commit()

    # Первые 10
    cursor.execute('SELECT * FROM insights ORDER BY id LIMIT 10')
    first_10 = cursor.fetchall()
    print("First 10:")
    for row in first_10:
       print(row)

    # Последние 10  
    cursor.execute('SELECT * FROM insights ORDER BY id DESC LIMIT 10')
    last_10 = cursor.fetchall()
    print("\nLast 10:")
    for row in last_10:
       print(row)

    conn.close()
paste_insights_to_db()