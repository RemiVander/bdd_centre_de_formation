from .auth_routes import auth_routes
from .home_routes import home_routes
from .calendar_routes import calendar_routes
from .registration_routes import registration_routes
from .session_routes import session_routes

def register_blueprints(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(calendar_routes)
    app.register_blueprint(registration_routes)
    app.register_blueprint(session_routes)
