import sqlite3

db_url = "data/california_purchases.db"

def execute_sql(query):
    with sqlite3.connect(db_url) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows