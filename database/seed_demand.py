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

routes = ["Blackrock DART → Belfield", "Belfield → Blackrock DART"]
now = datetime.utcnow()

# Shuttle only runs 8-10:30am and 4-6:30pm on weekdays
MORNING_HOURS = (8, 9, 10)
EVENING_HOURS = (16, 17, 18)
ACTIVE_HOURS = MORNING_HOURS + EVENING_HOURS

rows = []
for day_offset in range(90):
    date = now - timedelta(days=day_offset)
    if date.weekday() >= 5:  # skip weekends
        continue
    for hour in ACTIVE_HOURS:
        for route in routes:
            ts = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            base = 20 if hour in (8, 9, 17, 18) else 12
            count = max(0, int(random.gauss(base, 4)))
            rows.append((route, ts, count))

with conn.cursor() as cur:
    cur.executemany(
        "INSERT INTO demand_records (route, timestamp, passenger_count) VALUES (%s, %s, %s)",
        rows,
    )
conn.commit()
conn.close()
print(f"Inserted {len(rows)} demand records.")
