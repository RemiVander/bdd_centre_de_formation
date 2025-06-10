from flask import Blueprint, render_template, request, redirect, flash
from sqlmodel import Session, select
from app.database import engine
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.room import Room
from app.models.class_session import ClassSession
from app.models.user import User
from sqlalchemy.orm import selectinload
import json
from datetime import date

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def home():
    return render_template("home.html")



@main_routes.route("/calendar")
def calendar_view():
    with Session(engine) as session:
        sessions = session.exec(select(ClassSession)).all()
        
        rooms = session.exec(select(Room)).all()
        teachers = session.exec(select(Teacher)).all()
        
        rooms_dict = {room.id: room for room in rooms}
        teachers_dict = {teacher.id: teacher for teacher in teachers}
        
        events_by_room = {}
        all_events = []
        
        for s in sessions:
            room = rooms_dict.get(s.room_id)
            teacher = teachers_dict.get(s.teacher_id)
            
            event = {
                "id": s.id,
                "title": s.title,
                "start": s.start_date.isoformat(),
                "end": s.end_date.isoformat(),
                "description": s.description,
                "extendedProps": {
                    "teacher": teacher.name if teacher else "Non assigné", 
                    "room": room.name if room else "Non assignée", 
                    "room_id": s.room_id,
                    "max_capacity": s.max_capacity
                },
                "backgroundColor": f"hsl({hash(str(s.room_id)) % 360}, 70%, 60%)",
                "borderColor": f"hsl({hash(str(s.room_id)) % 360}, 70%, 50%)"
            }
            
            all_events.append(event)
            
            room_name = room.name if room else "Non assignée"
            if room_name not in events_by_room:
                events_by_room[room_name] = []
            events_by_room[room_name].append(event)
    
    return render_template(
        "calendar.html", 
        all_events=all_events,
        events_by_room=events_by_room,
        rooms=[{"id": r.id, "name": r.name} for r in rooms]

    )

@main_routes.route("/register", methods=["GET"])
def show_register_form():
    return render_template("register_user.html")

@main_routes.route("/register_teacher", methods=["POST"])
def register_user():
    name = request.form.get("name")
    surname = request.form.get("surname")
    age = request.form.get("age")
    email = request.form.get("email")
    speciality = request.form.get("speciality")

    with Session(engine) as session:
        existing_user = session.exec(select(Teacher).where(Teacher.email == email)).first()
        if existing_user:
            flash("A user with this email already exists!")
            return redirect("/error_user_exist")

        new_teacher = Teacher(
            name=name,
            surname=surname,
            age=age,
            email=email,
            is_active=True,
            role="teacher",
            speciality=speciality,
            hiring_date=date.today(),
            hours_rate=0.0,
            bio=None
        )

        session.add(new_teacher)
        session.commit()
        flash("Teacher successfully registered!")
        return redirect("/success")

@main_routes.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        birth_date = request.form["birth_date"]
        telephone = request.form.get("telephone")
        level_degree = request.form.get("level_degree")
        diploma = request.form.get("diploma")

        new_student = Student(
            name=name,
            surname=surname,
            email=email,
            is_active=True,
            role="student",
            birth_date=date.fromisoformat(birth_date),
            telephone=telephone,
            level_degree=level_degree,
            diploma=diploma
        )

        with Session(engine) as session:
            session.add(new_student)
            session.commit()
        return redirect("/success")
    
    return render_template("register_student.html")


@main_routes.route("/error_user_exist")
def error_user_exist():
    return render_template("error_user_exist.html")

from flask import render_template

@main_routes.route("/success")
def succes():
    return render_template("success.html")

@main_routes.route("/profile")
def profile():
    return render_template("profile.html")

@main_routes.route('/login')
def login():
    return render_template('login.html')

@main_routes.route('/logout')
def logout():
    return render_template('logout.html')


