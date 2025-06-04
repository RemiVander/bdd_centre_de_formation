from sqlmodel import  Field
from datetime import date
from typing import Optional

from models.user import User


class Teacher(User, table=True):
    __tablename__ = "teacher"

    speciality: str
    hiring_date: date 
    hours_rate: float = Field(ge=0) 
    bio: Optional[str] = None
