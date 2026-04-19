import sqlite3
import psycopg2
import json

# חיבור ל‑SQLite
sqlite_conn = sqlite3.connect('payments.db')
sqlite_cur = sqlite_conn.cursor()
sqlite_cur.execute("SELECT user_id, username, amount, currency, timestamp, status FROM payments")
rows = sqlite_cur.fetchall()

# חיבור ל‑PostgreSQL (בהנחה שרץ)
pg_conn = psycopg2.connect(
    host="localhost",
    database="slh_payments",
    user="slh",
    password="slh_pass"
)
pg_cur = pg_conn.cursor()
pg_cur.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        username TEXT,
        amount INTEGER,
        currency TEXT,
        timestamp TEXT,
        status TEXT
    )
''')
for row in rows:
    pg_cur.execute('''
        INSERT INTO payments (user_id, username, amount, currency, timestamp, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', row)
pg_conn.commit()
print(f"✅ Migrated {len(rows)} rows to PostgreSQL")
