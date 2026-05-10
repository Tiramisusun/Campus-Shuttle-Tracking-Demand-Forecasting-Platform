from flask import Blueprint, jsonify, request
from ..models.schedule import Schedule
from ..extensions import db
from ..services.cache import DistributedLock

schedules_bp = Blueprint("schedules", __name__)

@schedules_bp.get("/")
def list_schedules():
    route = request.args.get("route")
    query = Schedule.query
    if route:
        query = query.filter_by(route=route)
    return jsonify([s.to_dict() for s in query.all()])

@schedules_bp.post("/<int:schedule_id>/book")
def book_seat(schedule_id):
    with DistributedLock(f"schedule:{schedule_id}"):
        schedule = Schedule.query.get_or_404(schedule_id)
        if schedule.available_seats <= 0:
            return jsonify({"error": "No seats available"}), 409
        schedule.available_seats -= 1
        db.session.commit()
    return jsonify({"message": "Booked", "remaining_seats": schedule.available_seats})
