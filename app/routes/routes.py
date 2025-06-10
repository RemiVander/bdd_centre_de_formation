from flask import Blueprint, render_template, request, redirect, flash
from sqlmodel import Session, select
from app.database import engine
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.room import Room
from app.models.class_session import ClassSession, Requirement
from app.models.user import User
from sqlalchemy.orm import selectinload
import json
from datetime import date, datetime, timedelta

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

@main_routes.route("/register",methods=["GET", "POST"])
def show_register_form():
    return render_template("register_user.html")

@main_routes.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "GET":
        return render_template("register_teacher.html") 
    
    if request.method == "POST":
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
    if request.method == "GET":
        return render_template("register_student.html")
    
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        birth_date = request.form["birth_date"]
        telephone = request.form.get("telephone")
        level_degree = request.form.get("level_degree")
        diploma = request.form.get("diploma")
        
        with Session(engine) as session:
            existing_user = session.exec(select(Student).where(Student.email == email)).first()
            if existing_user:
                flash("A user with this email already exists!")
                return redirect("/error_user_exist")
                
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
            session.add(new_student)
            session.commit()
            flash("Student successfully registered!")
            return redirect("/success")


@main_routes.route("/error_user_exist")
def error_user_exist():
    return render_template("error_user_exist.html")

from flask import render_template

@main_routes.route("/success")
def succes():
    return render_template("success.html")

@main_routes.route("/success_session")
def succes_session():
    return render_template("success_session.html")


@main_routes.route("/create_session", methods=["GET", "POST"])
def create_session():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        session_date = request.form["session_date"]
        time_slot = request.form["time_slot"]
        max_capacity = int(request.form["max_capacity"])
        requirement_id = request.form.get("requirement_id") or None
        room_id = int(request.form["room_id"])
        teacher_id = int(request.form["teacher_id"])

        # Parse date
        date_obj = datetime.strptime(session_date, "%Y-%m-%d")

        # Parse time slot to start and end times
        start_str, end_str = time_slot.split('-')  # e.g. '8:00', '10:00'
        start_hour, start_minute = map(int, start_str.split(':'))
        end_hour, end_minute = map(int, end_str.split(':'))

        start_datetime = date_obj.replace(hour=start_hour, minute=start_minute)
        end_datetime = date_obj.replace(hour=end_hour, minute=end_minute)

        new_session = ClassSession(
            title=title,
            description=description,
            start_date= start_datetime,
            end_date= end_datetime,
            max_capacity= max_capacity,
            requirement_id=int(requirement_id) if requirement_id else None,
            room_id=room_id,
            teacher_id=teacher_id
        )

        with Session(engine) as session:
            new_session= ClassSession.model_validate(new_session)
            session.add(new_session)
            session.commit()
        return redirect("/success_session")
    
    with Session(engine) as session:
        titles = list(set(s.title for s in session.exec(select(ClassSession)).all()))
        teachers = session.exec(select(Teacher)).all()
        rooms = session.exec(select(Room)).all()
        requirements = session.exec(select(Requirement)).all()
    
    return render_template("create_session.html",titles=titles,teachers=teachers,rooms=rooms,requirements=requirements)
