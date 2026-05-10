from flask import Blueprint, jsonify, request
from flask_socketio import emit
from ..models.vehicle import Vehicle
from ..extensions import db, redis_client
from .. import socketio
import json

vehicles_bp = Blueprint("vehicles", __name__)

@socketio.on("connect")
def handle_connect():
    vehicles = Vehicle.query.all()
    emit("vehicles_initial", [v.to_dict() for v in vehicles])

@vehicles_bp.get("/")
def list_vehicles():
    cached = redis_client.get("vehicles:all")
    if cached:
        return jsonify(json.loads(cached))

    vehicles = Vehicle.query.all()
    data = [v.to_dict() for v in vehicles]
    redis_client.setex("vehicles:all", 30, json.dumps(data))
    return jsonify(data)

@vehicles_bp.get("/<int:vehicle_id>")
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(vehicle.to_dict())

@vehicles_bp.post("/<int:vehicle_id>/location")
def update_location(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json()
    vehicle.current_lat = data["lat"]
    vehicle.current_lng = data["lng"]
    db.session.commit()
    redis_client.delete("vehicles:all")
    socketio.emit("vehicle_update", {"id": vehicle.id, "lat": vehicle.current_lat, "lng": vehicle.current_lng})
    return jsonify(vehicle.to_dict())
