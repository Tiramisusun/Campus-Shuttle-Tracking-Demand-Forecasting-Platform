from flask import Blueprint, jsonify, request
from ..services.predictor import forecast_demand

forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.get("/")
def get_forecast():
    route = request.args.get("route", "main")
    periods = int(request.args.get("periods", 12))
    result = forecast_demand(route, periods)
    return jsonify(result)
