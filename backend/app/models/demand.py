from ..extensions import db
from datetime import datetime

class DemandRecord(db.Model):
    __tablename__ = "demand_records"

    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    passenger_count = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "route": self.route,
            "timestamp": self.timestamp.isoformat(),
            "passenger_count": self.passenger_count,
        }
