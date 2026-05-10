from ..extensions import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_lat = db.Column(db.Float, default=0.0)
    current_lng = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum("active", "idle", "maintenance"), default="idle")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "license_plate": self.license_plate,
            "capacity": self.capacity,
            "lat": self.current_lat,
            "lng": self.current_lng,
            "status": self.status,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
