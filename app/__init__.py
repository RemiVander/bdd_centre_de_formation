from flask import Flask
from app.routes.routes import main_routes

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "une_clé_ultra_secrète"
    
    app.register_blueprint(main_routes)

    return app
