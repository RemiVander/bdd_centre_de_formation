from flask import Blueprint, render_template

home_routes = Blueprint("home", __name__)

@home_routes.route("/")
def home():
    return render_template("home.html")

@home_routes.route("/error_user_exist")
def error_user_exist():
    return render_template("error_user_exist.html")

@home_routes.route("/success")
def success():
    return render_template("success.html")

@home_routes.route("/success_session")
def success_session():
    return render_template("success_session.html")
