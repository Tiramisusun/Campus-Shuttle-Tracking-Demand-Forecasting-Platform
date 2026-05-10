"""Generate 90 days of simulated demand data for model training."""
import random
import pymysql
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "password"),
    database="shuttle_tracking",
)

routes = ["Main Gate → Library", "Main Gate → Dorm A", "Library → Lab Building", "Dorm A → Cafeteria"]
now = datetime.utcnow()

rows = []
for day_offset in range(90):
    for hour in range(7, 23):
        for route in routes:
            ts = now - timedelta(days=day_offset) + timedelta(hours=hour - now.hour)
            # Peak hours: 8-9am, 12-13pm, 17-19pm
            base = 5
            if hour in (8, 9, 12, 13, 17, 18):
                base = 20
            elif hour in (7, 10, 11, 14, 15, 16, 19):
                base = 12
            count = max(0, int(random.gauss(base, 3)))
            rows.append((route, ts, count))

with conn.cursor() as cur:
    cur.executemany(
        "INSERT INTO demand_records (route, timestamp, passenger_count) VALUES (%s, %s, %s)",
        rows,
    )
conn.commit()
conn.close()
print(f"Inserted {len(rows)} demand records.")
