from sqlmodel import SQLModel, Field
from datetime import date, datetime, timezone
from typing import Optional

from models.user import User


class Student(User, table=True):
    __tablename__ = "student"

    birth_date: date
    level_degree: Optional[str] = None
    telephone: Optional[str] = None
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    diploma: Optional[str] = None
