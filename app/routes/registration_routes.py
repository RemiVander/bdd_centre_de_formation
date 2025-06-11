from flask import Blueprint, render_template, request, redirect, flash
from sqlmodel import Session, select
from datetime import date
from app.database import engine
from app.models.teacher import Teacher
from app.models.student import Student

"""
Module Flask pour la gestion de l'inscription des utilisateurs dans un centre de formation.

Ce module utilise Flask Blueprint pour définir des routes liées à l'inscription des enseignants
et des étudiants. Il interagit avec une base de données pour stocker les informations des utilisateurs
lors de leur inscription.

Routes principales :
    - register_choice : Affiche une page permettant à l'utilisateur de choisir entre
      s'inscrire en tant qu'enseignant ou étudiant.
    - register_teacher : Gère l'inscription des enseignants. Affiche le formulaire d'inscription
      et traite les données soumises pour créer un nouvel enseignant dans la base de données.
    - register_student : Gère l'inscription des étudiants. Affiche le formulaire d'inscription
      et traite les données soumises pour créer un nouvel étudiant dans la base de données.

Le module utilise SQLModel pour interagir avec la base de données et vérifier l'existence
d'utilisateurs avant de créer de nouveaux enregistrements.
"""

registration_routes = Blueprint("registration", __name__)

@registration_routes.route("/register")
def register_choice():
    """
    Affiche la page de choix d'inscription.

    Cette route affiche une page permettant à l'utilisateur de choisir s'il souhaite
    s'inscrire en tant qu'enseignant ou étudiant.

    Returns:
        Response: La page de choix d'inscription.
    """
    return render_template("register_user.html")

@registration_routes.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
    """
    Gère l'inscription des enseignants.

    Si la méthode est GET, affiche le formulaire d'inscription pour les enseignants.
    Si la méthode est POST, traite les données du formulaire pour créer un nouvel enseignant
    dans la base de données.

    Returns:
        Response: Redirige vers une page de succès ou affiche le formulaire d'inscription.
    """
    if request.method == "GET":
        return render_template("register_teacher.html")

    name = request.form["name"]
    surname = request.form["surname"]
    age = request.form["age"]
    email = request.form["email"]
    speciality = request.form["speciality"]

    with Session(engine) as session:
        if session.exec(select(Teacher).where(Teacher.email == email)).first():
            flash("Un utilisateur avec cet email existe déjà.")
            return redirect("/error_user_exist")

        teacher = Teacher(
            name=name, surname=surname, age=age, email=email, role="teacher",
            speciality=speciality, hiring_date=date.today(), is_active=True,
            hours_rate=0.0, bio=None
        )
        session.add(teacher)
        session.commit()

    flash("Inscription du professeur réussie.")
    return redirect("/success")

@registration_routes.route("/register_student", methods=["GET", "POST"])
def register_student():
    """
    Gère l'inscription des étudiants.

    Si la méthode est GET, affiche le formulaire d'inscription pour les étudiants.
    Si la méthode est POST, traite les données du formulaire pour créer un nouvel étudiant
    dans la base de données.

    Returns:
        Response: Redirige vers une page de succès ou affiche le formulaire d'inscription.
    """
    if request.method == "GET":
        return render_template("register_student.html")

    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]
    birth_date = request.form["birth_date"]
    telephone = request.form.get("telephone")
    level_degree = request.form.get("level_degree")
    diploma = request.form.get("diploma")

    with Session(engine) as session:
        if session.exec(select(Student).where(Student.email == email)).first():
            flash("Un utilisateur avec cet email existe déjà.")
            return redirect("/error_user_exist")

        student = Student(
            name=name, surname=surname, email=email, role="student",
            birth_date=date.fromisoformat(birth_date), telephone=telephone,
            level_degree=level_degree, diploma=diploma, is_active=True
        )
        session.add(student)
        session.commit()

    flash("Inscription de l'étudiant réussie.")
    return redirect("/success")
