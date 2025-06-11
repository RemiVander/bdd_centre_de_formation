from flask import Flask
from app.routes.auth_routes import auth_routes
from app.routes.calendar_routes import calendar_routes
from app.routes.home_routes import home_routes
from app.routes.registration_routes import registration_routes
from app.routes.session_routes import session_routes

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "une_clé_ultra_secrète"

    app.register_blueprint(auth_routes)
    app.register_blueprint(calendar_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(registration_routes)
    app.register_blueprint(session_routes)

    return app
