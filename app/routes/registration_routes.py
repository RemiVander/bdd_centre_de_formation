from flask import Blueprint, render_template, request, redirect, flash
from sqlmodel import Session, select
from datetime import date
from app.database import engine
from app.models.teacher import Teacher
from app.models.student import Student

registration_routes = Blueprint("registration", __name__)

@registration_routes.route("/register")
def register_choice():
    return render_template("register_user.html")

@registration_routes.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
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
