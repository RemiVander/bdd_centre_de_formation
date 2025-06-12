from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from sqlmodel import Session, select
from app.database import engine
from app.models.student import Student
from app.models.teacher import Teacher

"""
Module Flask pour la gestion de l'authentification des utilisateurs.

Ce module utilise Flask Blueprint pour définir des routes liées à l'authentification des utilisateurs,
notamment la connexion et la déconnexion. Il permet aux étudiants et aux enseignants de se connecter
en vérifiant leurs informations d'identification et gère les sessions utilisateur.

Routes principales :
    - login : Gère la connexion des utilisateurs. Affiche le formulaire de connexion et traite
      les informations d'identification soumises pour authentifier l'utilisateur.
    - logout : Gère la déconnexion des utilisateurs en effaçant les informations de session.

Le module utilise SQLModel pour interagir avec la base de données et vérifier les informations
d'identification des utilisateurs.
"""

auth_routes = Blueprint("auth", __name__)

@auth_routes.route('/login', methods=["GET", "POST"])
def login():
    """
    Gère la connexion des utilisateurs.

    Si la méthode est POST, traite les informations d'identification soumises pour authentifier
    l'utilisateur. Vérifie si l'utilisateur est un étudiant ou un enseignant et redirige vers
    la page du calendrier en cas de succès. Si la méthode est GET, affiche le formulaire de connexion.

    Returns:
        Response: Redirige vers la page du calendrier en cas de succès ou affiche le formulaire
        de connexion en cas d'échec.
    """
    if request.method == "POST":
        email = request.form.get('email')
        surname = request.form.get('surname')
        role = request.form.get('role')

        with Session(engine) as db_session:
            student = db_session.exec(select(Student).where(Student.email == email)).first()
            teacher = db_session.exec(select(Teacher).where(Teacher.email == email)).first()

            if student and student.surname == surname and role == "student":
                session['user'] = {
                    'email': email,
                    'surname': surname,
                    'role': 'student',
                    'id': student.id
                }
                return redirect('/calendar')

            elif teacher and teacher.surname == surname and role == "teacher":
                session['user'] = {
                    'email': email,
                    'surname': surname,
                    'role': 'teacher',
                    'id': teacher.id
                }
                return redirect('/calendar')

            else:
                flash('Veuillez vérifier vos identifiants.')
    
    return render_template('login.html')