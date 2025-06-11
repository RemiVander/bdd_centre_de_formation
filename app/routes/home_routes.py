from flask import Blueprint, render_template

"""
Module Flask pour la gestion des routes principales et des vues de base.

Ce module utilise Flask Blueprint pour définir des routes liées aux vues principales
de l'application, telles que la page d'accueil, les pages de succès et les pages d'erreur.
Il est conçu pour gérer les réponses de base de l'application et rediriger vers les
templates HTML appropriés.

Routes principales :
    - home : Affiche la page d'accueil de l'application.
    - error_user_exist : Affiche une page d'erreur indiquant qu'un utilisateur existe déjà.
    - success : Affiche une page de succès générique pour les opérations réussies.
    - success_session : Affiche une page de succès spécifique pour la création de sessions réussie.
"""

home_routes = Blueprint("home", __name__)

@home_routes.route("/")
def home():
    """
    Affiche la page d'accueil de l'application.

    Cette route est la racine de l'application et affiche la page d'accueil.

    Returns:
        Response: La page d'accueil de l'application.
    """
    return render_template("home.html")

@home_routes.route("/error_user_exist")
def error_user_exist():
    """
    Affiche une page d'erreur pour les utilisateurs existants.

    Cette route est utilisée pour informer l'utilisateur qu'un compte avec les informations
    fournies existe déjà.

    Returns:
        Response: La page d'erreur indiquant que l'utilisateur existe déjà.
    """
    return render_template("error_user_exist.html")

@home_routes.route("/success")
def success():
    """
    Affiche une page de succès générique.

    Cette route est utilisée pour confirmer à l'utilisateur qu'une opération s'est déroulée
    avec succès.

    Returns:
        Response: La page de succès générique.
    """
    return render_template("success.html")

@home_routes.route("/success_session")
def success_session():
    """
    Affiche une page de succès pour la création de sessions.

    Cette route est utilisée pour confirmer à l'utilisateur qu'une session a été créée
    avec succès.

    Returns:
        Response: La page de succès pour la création de sessions.
    """
    return render_template("success_session.html")
