from flask import Blueprint, jsonify, request
from ..models.demand import DemandRecord
from ..extensions import db
from ..services.cache import cache

demand_bp = Blueprint("demand", __name__)

@demand_bp.get("/")
def get_demand():
    route = request.args.get("route", "main")
    records = DemandRecord.query.filter_by(route=route).order_by(DemandRecord.timestamp).all()
    return jsonify([r.to_dict() for r in records])

@demand_bp.post("/")
def record_demand():
    data = request.get_json()
    record = DemandRecord(
        route=data["route"],
        passenger_count=data["passenger_count"],
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201
