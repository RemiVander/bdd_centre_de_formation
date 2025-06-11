from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from sqlmodel import Session as DBSession, select, func
from sqlalchemy import and_
from datetime import datetime, timezone
from app.database import engine
from app.models.class_session import ClassSession, Requirement
from app.models.room import Room
from app.models.teacher import Teacher
from app.models.registration import Registration

"""
Module Flask pour la gestion des sessions de cours dans un centre de formation.

Ce module utilise Flask Blueprint pour définir des routes liées à la création de sessions de cours,
à l'affichage des cours disponibles et à l'inscription des étudiants à ces sessions. Il interagit
avec une base de données pour récupérer et stocker les informations nécessaires.

Routes principales :
    - create_session : Permet de créer une nouvelle session de cours. Gère à la fois l'affichage
      du formulaire et la soumission des données du formulaire pour créer une session.
    - available_courses : Affiche toutes les sessions de cours disponibles aux étudiants pour
      inscription, avec des détails sur chaque session.
    - enroll : Permet à un étudiant de s'inscrire à une session de cours spécifique.

Le module utilise SQLModel pour interagir avec la base de données et récupérer les informations
nécessaires pour chaque vue.
"""

session_routes = Blueprint("session", __name__)

@session_routes.route("/create_session", methods=["GET", "POST"])
def create_session():
    """
    Crée une nouvelle session de cours.

    Si la méthode est POST, traite les données du formulaire pour créer une nouvelle session.
    Vérifie les conflits d'horaire et la validité de la salle avant de créer la session.
    Si la méthode est GET, affiche le formulaire de création de session avec les données nécessaires.

    Returns:
        Response: Redirige vers une page de succès ou affiche le formulaire de création de session.
    """

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        session_date = request.form["session_date"]
        time_slot = request.form["time_slot"]
        max_capacity = int(request.form.get("max_capacity", "0"))
        requirement_id = request.form.get("requirement_id") or None
        room_id = int(request.form["room_id"])
        teacher_id = session['user']['id'] if session.get('user') and session['user']['role'] == 'teacher' else int(request.form["teacher_id"])

        date_obj = datetime.strptime(session_date, "%Y-%m-%d")
        start_str, end_str = time_slot.split('-')
        start_hour, start_minute = map(int, start_str.split(':'))
        end_hour, end_minute = map(int, end_str.split(':'))
        start_datetime = date_obj.replace(hour=start_hour, minute=start_minute)
        end_datetime = date_obj.replace(hour=end_hour, minute=end_minute)

        with DBSession(engine) as db:
            room = db.exec(select(Room).where(Room.id == room_id)).first()
            if not room or max_capacity > room.capacite:
                flash("Salle invalide ou capacité dépassée.")
                return redirect("/create_session")

            overlap = db.exec(
                select(ClassSession).where(
                    and_(
                        ClassSession.room_id == room_id,
                        ClassSession.start_date < end_datetime,
                        ClassSession.end_date > start_datetime
                    )
                )
            ).all()

            if overlap:
                flash("Conflit d'horaire détecté.")
                return redirect("/create_session")

            session_obj = ClassSession(
                title=title,
                description=description,
                start_date=start_datetime,
                end_date=end_datetime,
                max_capacity=max_capacity,
                requirement_id=int(requirement_id) if requirement_id else None,
                room_id=room_id,
                teacher_id=teacher_id
            )
            db.add(session_obj)
            db.commit()
            flash("Session créée avec succès.")
            return redirect("/success_session")

    with DBSession(engine) as db:
        titles = list(set(s.title for s in db.exec(select(ClassSession)).all()))
        teachers = db.exec(select(Teacher)).all()
        rooms = db.exec(select(Room)).all()
        requirements = db.exec(select(Requirement)).all()

    return render_template("create_session.html", titles=titles, teachers=teachers, rooms=rooms, requirements=requirements)

@session_routes.route("/available_courses")
def available_courses():
    """
    Affiche les sessions de cours disponibles pour inscription.

    Récupère toutes les sessions de cours disponibles et les informations associées,
    telles que la salle, la capacité maximale et le nombre actuel d'inscriptions.

    Returns:
        Response: Affiche la page des cours disponibles avec les données des sessions.
    """

    with DBSession(engine) as db:
        sessions = db.exec(select(ClassSession)).all()
        rooms = db.exec(select(Room)).all()
        room_map = {r.id: r for r in rooms}
        enrollments = db.exec(select(Registration.session_id, func.count(Registration.id).label("current_enrollment")).group_by(Registration.session_id)).all()
        enrollment_dict = {sid: count for sid, count in enrollments}

        all_events = []
        for s in sessions:
            current = enrollment_dict.get(s.id, 0)
            if current < s.max_capacity:
                room = room_map.get(s.room_id)
                if room:
                    all_events.append({
                        "id": s.id,
                        "title": s.title,
                        "start": s.start_date.isoformat(),
                        "end": s.end_date.isoformat(),
                        "description": s.description,
                        "extendedProps": {
                            "room": room.name,
                            "max_capacity": s.max_capacity,
                            "current_enrollment": current
                        },
                        "backgroundColor": f"hsl({hash(str(s.room_id)) % 360}, 70%, 60%)",
                        "borderColor": f"hsl({hash(str(s.room_id)) % 360}, 70%, 50%)"
                    })

    return render_template("available_courses.html", all_events=all_events)

@session_routes.route("/enroll/<int:session_id>", methods=["POST", "GET"])
def enroll(session_id):
    """
    Permet à un étudiant de s'inscrire à une session de cours spécifique.

    Vérifie si l'utilisateur est connecté en tant qu'étudiant et s'il n'est pas déjà inscrit
    à la session. Si les conditions sont remplies, crée une nouvelle inscription.

    Args:
        session_id (int): L'identifiant de la session à laquelle l'étudiant souhaite s'inscrire.

    Returns:
        Response: Redirige vers la page des cours disponibles avec un message de succès ou d'erreur.
    """
    
    if 'user' not in session or session['user']['role'] != 'student':
        flash("Connectez-vous en tant qu'étudiant.")
        return redirect(url_for("auth.login"))

    student_id = session['user']['id']
    with DBSession(engine) as db:
        already_registered = db.exec(
            select(Registration).where(
                Registration.student_id == student_id,
                Registration.session_id == session_id
            )
        ).first()

        if already_registered:
            flash("Déjà inscrit à ce cours.")
            return redirect(url_for("session.available_courses"))

        new_reg = Registration(
            student_id=student_id,
            session_id=session_id,
            registration_date=datetime.now(timezone.utc),
            registration_status='confirmed',
            presence=False
        )
        db.add(new_reg)
        db.commit()
        flash("Inscription réussie.")

    return redirect(url_for("session.available_courses"))
