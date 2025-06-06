from sqlmodel import  Field
from datetime import date
from typing import Optional
from pydantic import model_validator
from app.models.user import User


class Teacher(User, table=True):
    __tablename__ = "teacher"

    speciality: str
    hiring_date: date 
    hours_rate: float = Field(ge=0) 
    bio: Optional[str] = None

    @model_validator(mode='after')
    def check_hiring_date(self):
        if self.hiring_date >= date.today():
            raise ValueError("hiring date must be before date today")
        return self
