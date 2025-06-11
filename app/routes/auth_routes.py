from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from sqlmodel import Session, select
from app.database import engine
from app.models.student import Student
from app.models.teacher import Teacher

auth_routes = Blueprint("auth", __name__)

@auth_routes.route('/login', methods=["GET", "POST"])
def login():
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

@auth_routes.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')
