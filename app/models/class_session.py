from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional
from pydantic import model_validator

class ClassSession(SQLModel, table=True):
    __tablename__ = "class_session"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    max_capacity: int
    statut_id: int = Field(default=1, foreign_key="status.id")  # Supposons que 'OPEN' = id 1 dans status
    requirement_id: Optional[int] = Field(default=None, foreign_key="requirement.id")
    room_id: int = Field(foreign_key="room.id")
    teacher_id: int = Field(foreign_key="teacher.id")

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("start must be before end date")
        return self

    
class Requirement(SQLModel, table = True):
    __tablename__ = "requirement"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True)

class Status(SQLModel, table = True):
    __tablename__ = "status"
    id : int | None = Field(default=None, primary_key=True)
    type : str = Field(unique=True)
