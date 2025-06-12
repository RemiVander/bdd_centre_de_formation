from flask import Blueprint, render_template
from sqlmodel import Session, select
from app.database import engine
from app.models.class_session import ClassSession
from app.models.room import Room
from app.models.teacher import Teacher

"""
Module Flask pour l'affichage et la gestion d'un calendrier des sessions de cours.

Ce module utilise Flask Blueprint pour définir des routes liées à l'affichage d'un calendrier
interactif des sessions de cours. Il récupère les informations sur les sessions, les salles et
les enseignants depuis la base de données et les organise pour être affichées dans un calendrier.

Routes principales :
    - calendar_view : Récupère toutes les sessions de cours, les salles et les enseignants
      depuis la base de données, et les organise pour être affichées dans un calendrier.
      Les événements du calendrier sont colorés en fonction de la salle et regroupés par salle.

Le module utilise SQLModel pour interagir avec la base de données et récupérer les informations
nécessaires pour chaque vue.
"""

calendar_routes = Blueprint("calendar", __name__)

@calendar_routes.route("/calendar")
def calendar_view():
    """
    Affiche un calendrier des sessions de cours.

    Cette route récupère toutes les sessions de cours, les salles et les enseignants
    depuis la base de données. Elle organise ces informations en événements pour un
    calendrier interactif, où chaque événement est coloré en fonction de la salle
    et contient des informations supplémentaires telles que l'enseignant et la capacité
    maximale de la salle.

    Returns:
        Response: La page du calendrier avec les événements organisés et colorés,
        ainsi que les événements regroupés par salle.
    """
    with Session(engine) as session:
        sessions = session.exec(select(ClassSession)).all()
        rooms = session.exec(select(Room)).all()
        teachers = session.exec(select(Teacher)).all()

        rooms_dict = {room.id: room for room in rooms}
        teachers_dict = {teacher.id: teacher for teacher in teachers}
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

        events_by_room = {}
        for event in all_events:
            events_by_room.setdefault(event["extendedProps"]["room"], []).append(event)

        return render_template("calendar.html", all_events=all_events, events_by_room=events_by_room, rooms=rooms)
