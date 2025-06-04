from sqlmodel import SQLModel, create_engine, Session, select
from models.teacher import Teacher
from models.admin import Admin
from datetime import date
from models.user import User
engine = create_engine("sqlite:///centre_de_formation.db", echo=True)


SQLModel.metadata.create_all(engine)



with Session(engine) as session:
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

    admin = Admin(
        name="John",
        surname="Doe",
        email="jd@example.com",
        is_active=True,
        role="admin",
        hiring_date=date(2018, 5, 15)
    )


    session.add(teacher)
    session.add(admin)
    session.commit()

    result = session.exec(select(Teacher)).all()
    print(result)
