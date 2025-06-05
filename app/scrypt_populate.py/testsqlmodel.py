import sys, os
sys.path.append(os.getcwd())
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, func
from faker import Faker
import random
from app.models.teacher import Teacher
from app.models.room import Room
from app.models.class_session import ClassSession, Status, Requirement
from app.models.student import Student
from app.models.admin import Admin
from app.models.equipments import Equipments, computer_lab_equipment
from datetime import date, timedelta
from app.database import engine


SQLModel.metadata.create_all(engine)


fake = Faker(locale="fr_FR")


# Fonction pour générer des données fictives teacher et les insérer dans la base de données
def populate_table_teacher(num_teacher: int = 10):
    with Session(engine) as session:
        for _ in range(num_teacher):
            teacher = Teacher(
                name=fake.unique.first_name(),
                surname=fake.unique.user_name(),
                age=fake.random_int(min=18, max=80),
                email=fake.email(),
                is_active=True,
                role="teacher",
                speciality="Data Science",
                hiring_date=date(2021, 5, 15),
                hours_rate=60.0,
                bio=fake.job()
            )
            session.add(teacher)
        session.commit()


# Fonction pour générer des salles fictives et les insérer dans la base de données
def populate_table_room(num_room: int = 10):
    with Session(engine) as session:
        for _ in range(num_room):
            room = Room(
                name=fake.unique.first_name(),
                capacite=fake.random_int(min=1, max=10),
                localization=fake.street_address(),
                is_active=True,
                role="user"
            )
            session.add(room)
        session.commit()

# Fonction pour générer des requirements
def populate_table_requirements(num_requirements: int = 10):
    with Session(engine) as session:
        for _ in range(num_requirements):
            requipment_entry = Requirement(
                name = fake.unique.job()
            )
            session.add(requipment_entry)
        session.commit()

# Fonction pour générer les status 
def populate_table_status():
    with Session(engine) as session:
        st1 = Status(type='OPEN')
        st2 = Status(type='ARCHIVED')
        st3 = Status(type='CLOSED')
        session.add(st1)
        session.add(st2)
        session.add(st3)
        session.commit()

# Fonction pour générer des sessions fictives et les insérer dans la base de données
def populate_table_class_session(num_class_session: int = 10):
    with Session(engine) as session:
        teachers = session.exec(select(Teacher)).all()
        rooms = session.exec(select(Room)).all()
        statuses = session.exec(select(Status)).all()
        requirement = session.exec(select(Requirement)).all()

        for _ in range(num_class_session):
            room = random.choice(rooms)
            teacher = random.choice(teachers)
            status = random.choice(statuses)
            requirements = random.choice(requirement)
            
            start = fake.date_time_this_year()
            end = start + timedelta(days=random.randint(1, 5))

            cs = ClassSession(
                title=fake.catch_phrase(),
                description=fake.sentence(),
                start_date=start,
                end_date=end,
                max_capacity=random.randint(1, room.capacite),
                statut_id=status.id,
                room_id=room.id,
                teacher_id=teacher.id,
                requirement_id=requirements.id
            )
            session.add(cs)
        session.commit()

# Fonction pour générer des étudiants fictifs et les insérer dans la base de données
def populate_table_student(num_student: int = 1):
    diploma_list = ["Data Engineer", "Data Scientist", "Data Analyst", "DevOps"]
    with Session(engine) as session:
        for _ in range(num_student):
            student = Student(
                name=fake.unique.first_name(),
                surname=fake.unique.last_name(),
                email=fake.email(),
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=30),
                level_degree=random.randint(1, 7),
                telephone=random.randint(1, 100),
                registration_date=date(2021, 5, 15),
                diploma=random.choice(diploma_list),
                is_active = fake.boolean(),
                role = "student"
            )
            session.add(student)
        session.commit()

# Fonction pour générer des admins fictifs et les insérer dans la base de données
def populate_table_admin(num_admin: int = 1):
    with Session(engine) as session:
        for _ in range(num_admin):
            admin = Admin(
                name=fake.unique.first_name(),
                surname=fake.unique.last_name(),
                email=fake.email(),
                hiring_date=date(2021, 5, 15),
                is_active = fake.boolean(),
                role = "admin"
            )
            session.add(admin)
        session.commit()

# Fonction pour générer des equipements fictifs et les insérer dans la base de données
def populate_table_equipments(num_equipments: int = 1):
    with Session(engine) as session:
        for equipment in computer_lab_equipment:
            equipment_entry = Equipments(
                name=equipment["name"],
                description=equipment["description"]
            )
            session.add(equipment_entry)
        session.commit()


# Appeler la fonction pour peupler la table avec 10 héros fictifs
populate_table_teacher(10)
populate_table_room(6)
populate_table_student(20)
populate_table_admin(2)
populate_table_requirements(10)
populate_table_status()
populate_table_class_session(5)
populate_table_equipments(2)

