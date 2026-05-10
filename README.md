# Campus Shuttle Tracking & Demand Forecasting Platform

A full-stack cloud platform for real-time campus shuttle tracking and passenger demand forecasting, built with Python/Flask, React, MySQL, Redis, and deployed on AWS.

---

## Features

- **Real-time GPS tracking** — live shuttle positions via WebSocket push
- **Schedule & seat booking** — Redis distributed lock prevents concurrent overselling
- **Demand forecasting** — Prophet time-series model predicts hourly passenger load
- **Data dashboard** — historical demand visualization by route and time

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 · Flask · Flask-SocketIO |
| Frontend | React 18 · Vite · Recharts · Leaflet |
| Database | MySQL 8 (AWS RDS) |
| Cache / Lock | Redis |
| ML | Prophet (Meta) |
| Cloud | AWS EC2 · RDS · S3 |
| CI/CD | GitLab CI/CD |

---

## Architecture

```
React Frontend (Vite)
       │
       │  HTTP / WebSocket
       ▼
Flask REST API
  ├── /api/vehicles     — real-time location
  ├── /api/schedules    — booking with distributed lock
  ├── /api/demand       — historical records
  └── /api/forecast     — Prophet prediction
       │
  ┌────┴────────────┐
MySQL (AWS RDS)   Redis
                  ├── schedule cache (TTL 60s)
                  └── distributed lock (seat booking)
```

---

## Project Structure

```
shuttle-tracking/
├── backend/
│   ├── app/
│   │   ├── __init__.py         # app factory
│   │   ├── config.py
│   │   ├── extensions.py       # db, redis
│   │   ├── models/
│   │   │   ├── vehicle.py
│   │   │   ├── schedule.py
│   │   │   └── demand.py
│   │   ├── routes/
│   │   │   ├── vehicles.py
│   │   │   ├── schedules.py
│   │   │   ├── demand.py
│   │   │   └── forecast.py
│   │   └── services/
│   │       ├── cache.py        # Redis cache decorator + DistributedLock
│   │       └── predictor.py    # Prophet model
│   ├── requirements.txt
│   └── run.py
├── database/
│   ├── schema.sql              # DDL + seed vehicles/schedules
│   └── seed_demand.py          # generate 90-day training data
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map/            # Leaflet real-time map
│   │   │   ├── Schedule/       # schedule list + booking
│   │   │   ├── Forecast/       # demand forecast chart
│   │   │   └── Dashboard/      # historical bar chart
│   │   ├── hooks/
│   │   │   └── useWebSocket.js # Socket.IO vehicle updates
│   │   ├── services/
│   │   │   └── api.js          # Axios API client
│   │   └── App.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── .gitlab-ci.yml
```

---

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 20+ (npm 10+)
- MySQL 8.0 — download from [dev.mysql.com/downloads/mysql](https://dev.mysql.com/downloads/mysql/), install the macOS `.dmg` package; the root password is set during installation
- Redis 5+

See [requirements.txt](requirements.txt) for a full list of system and package dependencies.

### 1. Database

MySQL is installed to `/usr/local/mysql` and starts automatically after installation. If it's not running, start it via **System Settings → MySQL → Start MySQL Server**.

```bash
mysql -u root -p < database/schema.sql
```

Generate 90 days of simulated passenger demand data (weekdays only, morning 8–10:30 and evening 16–18:30) for the Prophet forecasting model:

```bash
cd database
pip install pymysql python-dotenv
python seed_demand.py
# Inserts demand records for routes: Blackrock DART → Belfield, Belfield → Blackrock DART
```

Simulate real-time GPS movement of the 3 shuttle buses along the Blackrock–Belfield route (requires backend to be running):

```bash
python simulate_gps.py
# Buses move between: Blackrock DART Station → UCD Smurfit → UCD Belfield Village
# Position updates every 2 seconds via POST /api/vehicles/:id/location
```

### 2. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your DB credentials
```

`.env`:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/shuttle_tracking
REDIS_URL=redis://localhost:6379/0
```

```bash
python run.py
# API running at http://localhost:5000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# UI running at http://localhost:5173
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vehicles/` | List all vehicles with current GPS |
| POST | `/api/vehicles/:id/location` | Update vehicle GPS position |
| GET | `/api/schedules/?route=<name>` | Query schedules by route |
| POST | `/api/schedules/:id/book` | Book a seat (distributed lock) |
| GET | `/api/demand/?route=<name>` | Historical passenger records |
| POST | `/api/demand/` | Record new demand entry |
| GET | `/api/forecast/?route=<name>&periods=12` | Prophet forecast (next N hours) |

### Example

```bash
# Get all vehicles
curl http://localhost:5000/api/vehicles/

# Book a seat
curl -X POST http://localhost:5000/api/schedules/1/book

# Get 12-hour forecast
curl "http://localhost:5000/api/forecast/?route=Main+Gate+%E2%86%92+Library&periods=12"
```

---

## Key Technical Decisions

### Redis Distributed Lock for Seat Booking

Concurrent booking requests can cause overselling when multiple transactions read the same `available_seats` value before either commits. A Redis `SET NX EX` lock serializes access per schedule:

```python
with DistributedLock(f"schedule:{schedule_id}"):
    schedule = Schedule.query.get(schedule_id)
    if schedule.available_seats <= 0:
        return 409
    schedule.available_seats -= 1
    db.session.commit()
```

### Demand Forecasting with Prophet

Prophet handles campus demand patterns well — weekly seasonality (weekday vs. weekend) and daily peaks (rush hours). After training on 90 days of historical data:

```python
model = Prophet(interval_width=0.95)
model.fit(df)           # df columns: ds (datetime), y (passenger_count)
forecast = model.predict(future)
```

The API returns predicted value plus 95% confidence interval (`yhat_lower`, `yhat_upper`).

---

## AWS Deployment

### Infrastructure

| Resource | Purpose |
|----------|---------|
| EC2 (t3.small) | Flask API + Gunicorn |
| RDS (db.t3.micro) | MySQL 8 |
| S3 | React build static assets |
| ElastiCache | Redis |

### EC2 Setup

```bash
# On EC2 instance
git clone <repo-url> /app/shuttle-tracking
cd /app/shuttle-tracking/backend
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend to S3

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket-name --delete
```

---

## CI/CD (GitLab)

Three-stage pipeline defined in `.gitlab-ci.yml`:

```
test  →  build  →  deploy
```

- **test**: runs pytest on every MR
- **build**: compiles React bundle, stores as artifact
- **deploy**: SSH into EC2, pulls latest, restarts Gunicorn (main branch only)

Required GitLab CI variables: `EC2_SSH_KEY`, `EC2_HOST`

---

## Screenshots

> Add screenshots here after running the app locally.

- Real-time map with shuttle markers
- Schedule list with booking button
- Demand forecast line chart (with confidence interval)
- Historical demand bar chart by hour

---

## License

MIT
