from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, func
from faker import Faker
from models.teacher import Teacher
from models.admin import Admin
from models.room import Room
from main import SQLModel,engine, Session, select
from datetime import date


fake = Faker()


# Fonction pour générer des données fictives et les insérer dans la base de données
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

# Appeler la fonction pour peupler la table avec 10 héros fictifs
populate_table_teacher(10)


