from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from sqlalchemy.sql import func
from typing import Optional

class Registration(SQLModel, table = True):
    __tablename__ = "registration"


    id : int | None = Field(default=None, primary_key=True)
    student_id : int = Field(unique=True, foreign_key='student.id')
    session_id : int = Field(unique=True, foreign_key='session.id') 
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    registration_status :str 
    presence : Optional[bool]