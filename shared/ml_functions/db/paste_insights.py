import sqlite3
import sys
import os
sys.path.append(os.path.abspath("shared/ml_functions"))
from shared.ml_functions.predict_function import predict

def paste_insights_to_db():
    predictions = predict()
    print(predictions)
    conn = sqlite3.connect('data/insights.db')
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
#paste_insights_to_db()