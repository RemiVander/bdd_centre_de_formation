from sqlmodel import SQLModel, create_engine, Session, select
from models.teacher import Teacher
from datetime import date
from models.user import User
engine = create_engine("sqlite:///test.db", echo=True)


SQLModel.metadata.create_all(engine)

teacher = Teacher(
    name="Alice",
    surname="Durand",
    email="alice@example.com",
    is_active=True,
    role="teacher",
    speciality="Data Science",
    hiring_date=date(2021, 5, 15),
    hours_rate=60.0,
    bio="Experte en machine learning."
)

with Session(engine) as session:
    session.add(teacher)
    session.commit()

    result = session.exec(select(Teacher)).all()
    print(result)
