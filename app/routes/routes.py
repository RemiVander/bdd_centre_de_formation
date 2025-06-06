from flask import Blueprint, render_template
from sqlmodel import Session, select
from app.database import engine
from app.models.teacher import Teacher
from app.models.room import Room
from app.models.class_session import ClassSession
from sqlalchemy.orm import selectinload
import json

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def home():
    with Session(engine) as session:
        teachers = session.exec(select(Teacher)).all()
    return render_template("home.html", teachers=teachers)


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