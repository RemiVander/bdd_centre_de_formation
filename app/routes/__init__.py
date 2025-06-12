from .auth_routes import auth_routes
from .home_routes import home_routes
from .calendar_routes import calendar_routes
from .registration_routes import registration_routes
from .session_routes import session_routes

def register_blueprints(app):
    """
    Enregistre tous les blueprints de l'application Flask.

    Cette fonction est utilisée pour centraliser l'enregistrement des différents blueprints
    de l'application Flask. Elle importe et enregistre les blueprints liés à l'authentification,
    à la page d'accueil, au calendrier, à l'inscription des utilisateurs et à la gestion des sessions.

    Args:
        app (Flask): L'instance de l'application Flask à laquelle les blueprints seront enregistrés.

    The blueprints registered are:
        - auth_routes: Routes liées à l'authentification des utilisateurs.
        - home_routes: Routes liées à la page d'accueil et aux vues de base.
        - calendar_routes: Routes liées à l'affichage et à la gestion du calendrier des sessions.
        - registration_routes: Routes liées à l'inscription des enseignants et des étudiants.
        - session_routes: Routes liées à la création et à la gestion des sessions de cours.
    """
    app.register_blueprint(auth_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(calendar_routes)
    app.register_blueprint(registration_routes)
    app.register_blueprint(session_routes)
