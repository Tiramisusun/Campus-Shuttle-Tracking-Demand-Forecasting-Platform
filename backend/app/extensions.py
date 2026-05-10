import redis
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)
