from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from .extensions import db, redis_client
from .config import Config

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from .routes.vehicles import vehicles_bp
    from .routes.schedules import schedules_bp
    from .routes.demand import demand_bp
    from .routes.forecast import forecast_bp

    app.register_blueprint(vehicles_bp, url_prefix="/api/vehicles")
    app.register_blueprint(schedules_bp, url_prefix="/api/schedules")
    app.register_blueprint(demand_bp, url_prefix="/api/demand")
    app.register_blueprint(forecast_bp, url_prefix="/api/forecast")

    return app
