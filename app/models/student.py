from sqlmodel import Field
from datetime import date, datetime, timezone
from typing import Optional
from pydantic import model_validator
from app.models.user import User


class Student(User, table=True):
    __tablename__ = "student"

    birth_date: date 
    level_degree: Optional[int] = None
    telephone: Optional[int] = None
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    diploma: Optional[str] = None

    @model_validator(mode='after')
    def check_legal_age(self):
        if self.birth_date >= date(2009,6,1):
            raise ValueError("student is underage")
        return self
