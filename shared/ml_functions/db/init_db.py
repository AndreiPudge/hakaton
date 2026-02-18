import sqlite3
from pathlib import Path

database_path = Path("/data/insights.db")

def init_database():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS insights')

    cursor.execute('''
        CREATE TABLE insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight FLOAT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database has been initialized.")

if __name__ == "__main__":
    init_database()