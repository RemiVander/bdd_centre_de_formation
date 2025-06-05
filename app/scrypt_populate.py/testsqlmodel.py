import sys, os
sys.path.append(os.getcwd())

from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, func
from faker import Faker
import random

from app.models.teacher import Teacher
from app.models.user import User
from app.models.room import Room
from app.models.student import Student
from app.models.admin import Admin


from datetime import date
engine = create_engine("sqlite:///centre_de_formation.db", echo=True)
SQLModel.metadata.create_all(engine)

fake = Faker()

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
                bio="Experte en machine learning."
            )

            session.add(teacher)
    
        session.commit()

#  Fonction pour générer des données fictives teacher et les insérer dans la base de données
# def populate_table_user(num_user: int = 10):
#     with Session(engine) as session:
#         for _ in range(num_user):
#             user = User(
#                 name=fake.unique.first_name(),
#                 surname=fake.unique.last_name(),
#                 email=fake.email(),
#                 creation_date= fake.date(),
#                 is_active=True,
#                 role="user"             
#             )

#             session.add(user)
    
#         session.commit()

# # Fonction pour générer des salles fictives et les insérer dans la base de données
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

# # Fonction pour générer des étudiants fictifs et les insérer dans la base de données
def populate_table_student(num_student: int = 1):
    with Session(engine) as session:
        for _ in range(num_student):
            student = Student(
                name=fake.unique.first_name(),
                surname=fake.unique.last_name(),
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=30),
                level_degree=random.randint(1, 7),
                telephone=random.randint(1, 100),
                registration_date=date(2021, 5, 15),
                diploma="Data engineer"
            )

            session.add(student)
    
        session.commit()

# Appeler la fonction pour peupler la table avec 10 héros fictifs
populate_table_teacher(10)
#populate_table_user(20)
populate_table_room(6)
populate_table_student(2)

