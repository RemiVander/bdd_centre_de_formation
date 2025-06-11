from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from sqlmodel import Session, select, func
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from datetime import date, datetime, timedelta, timezone
import json

from app.database import engine
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.room import Room
from app.models.registration import Registration
from app.models.class_session import ClassSession, Requirement
from app.models.user import User

main_routes = Blueprint("main", __name__)
role_id = []

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
            events_by_room.setdefault(room_name, []).append(event)
    
    return render_template(
        "calendar.html", 
        all_events=all_events,
        events_by_room=events_by_room,
        rooms=[{"id": r.id, "name": r.name} for r in rooms]
    )

@main_routes.route("/register", methods=["GET", "POST"])
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

@main_routes.route("/success")
def succes():
    return render_template("success.html")

@main_routes.route("/success_session")
def succes_session():
    return render_template("success_session.html")

@main_routes.route('/login', methods=["GET", "POST"])
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
                flash('Please check your login details and try again.')

    return render_template('login.html')

@main_routes.route('/logout')
def logout():
    return render_template('logout.html')

@main_routes.route("/create_session", methods=["GET", "POST"])
def create_session():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        session_date = request.form["session_date"]
        time_slot = request.form["time_slot"]

        max_capacity_str = request.form.get("max_capacity", "").strip()
        if not max_capacity_str.isdigit() or int(max_capacity_str) <= 0:
            flash("Capacité maximale invalide (doit être un entier positif).")
            return redirect("/create_session")
        max_capacity = int(max_capacity_str)

        requirement_id = request.form.get("requirement_id") or None
        room_id = int(request.form["room_id"])

        teacher_id = session['user']['id'] if 'user' in session and session['user']['role'] == 'teacher' else int(request.form["teacher_id"])

        date_obj = datetime.strptime(session_date, "%Y-%m-%d")
        start_str, end_str = time_slot.split('-')
        start_hour, start_minute = map(int, start_str.split(':'))
        end_hour, end_minute = map(int, end_str.split(':'))
        start_datetime = date_obj.replace(hour=start_hour, minute=start_minute)
        end_datetime = date_obj.replace(hour=end_hour, minute=end_minute)

        with Session(engine) as session:
            selected_room = session.exec(select(Room).where(Room.id == room_id)).first()
            if not selected_room:
                flash("Salle non trouvée!")
                return redirect("/create_session")

            if max_capacity > selected_room.capacite:
                flash(f"Erreur: La capacité demandée ({max_capacity}) dépasse la capacité de la salle ({selected_room.capacite})")
                return redirect("/create_session")

            conflicting_sessions = session.exec(
                select(ClassSession).where(
                    and_(
                        ClassSession.room_id == room_id,
                        ClassSession.start_date < end_datetime,
                        ClassSession.end_date > start_datetime
                    )
                )
            ).all()

            if conflicting_sessions:
                conflict_details = [
                    f"{conflict.title} ({conflict.start_date.strftime('%H:%M')} - {conflict.end_date.strftime('%H:%M')})"
                    for conflict in conflicting_sessions
                ]
                flash(f"Erreur: Conflit de créneaux détecté dans cette salle avec: {', '.join(conflict_details)}")
                return redirect("/create_session")

            new_session = ClassSession(
                title=title,
                description=description,
                start_date=start_datetime,
                end_date=end_datetime,
                max_capacity=max_capacity,
                requirement_id=int(requirement_id) if requirement_id else None,
                room_id=room_id,
                teacher_id=teacher_id
            )

            session.add(new_session)
            session.commit()
            flash("Session créée avec succès!")
            return redirect("/success_session")

    with Session(engine) as session:
        titles = list(set(s.title for s in session.exec(select(ClassSession)).all()))
        teachers = session.exec(select(Teacher)).all()
        rooms = session.exec(select(Room)).all()
        requirements = session.exec(select(Requirement)).all()
    
    return render_template("create_session.html", titles=titles, teachers=teachers, rooms=rooms, requirements=requirements)

@main_routes.route("/available_courses")
def available_courses():
    with Session(engine) as session:
        sessions = session.exec(select(ClassSession)).all()
        rooms = session.exec(select(Room)).all()

        rooms_dict = {room.id: room for room in rooms}

        statement = select(Registration.session_id, func.count(Registration.id).label('current_enrollment')).group_by(Registration.session_id)
        session_enrollments = session.exec(statement).all()

        enrollments_dict = {session_id: current_enrollment for session_id, current_enrollment in session_enrollments}

        all_events = []
        for s in sessions:
            current_enrollment = enrollments_dict.get(s.id, 0)
            if current_enrollment < s.max_capacity:
                room = rooms_dict.get(s.room_id)
                if room:
                    event = {
                        "id": s.id,
                        "title": s.title,
                        "start": s.start_date.isoformat(),
                        "end": s.end_date.isoformat(),
                        "description": s.description,
                        "extendedProps": {
                            "room": room.name,
                            "max_capacity": s.max_capacity,
                            "current_enrollment": current_enrollment
                        },
                        "backgroundColor": f"hsl({hash(str(s.room_id)) % 360}, 70%, 60%)",
                        "borderColor": f"hsl({hash(str(s.room_id)) % 360}, 70%, 50%)"
                    }
                    all_events.append(event)

    return render_template("available_courses.html", all_events=all_events)

@main_routes.route('/enroll/<int:session_id>', methods=['GET', 'POST'])
def enroll(session_id):
    if 'user' not in session or session['user']['role'] != 'student':
        flash('Vous devez être connecté en tant qu\'étudiant pour vous inscrire à un cours.')
        return redirect(url_for('main.login'))

    student_id = session['user']['id']

    with Session(engine) as db_session:
        existing_registration = db_session.exec(
            select(Registration).where(
                Registration.student_id == student_id,
                Registration.session_id == session_id
            )
        ).first()

        if existing_registration:
            flash('Vous êtes déjà inscrit à ce cours.')
            return redirect(url_for('main.available_courses'))

        new_registration = Registration(
            student_id=student_id,
            session_id=session_id,
            registration_date=datetime.now(timezone.utc),
            registration_status='confirmed',
            presence=False
        )

        db_session.add(new_registration)
        db_session.commit()
        flash('Inscription réussie!')

    return redirect(url_for('main.available_courses'))
