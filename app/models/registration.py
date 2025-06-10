from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import UniqueConstraint

class Registration(SQLModel, table=True):
    __tablename__ = "registration"

    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    session_id: int = Field(foreign_key="class_session.id")
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    registration_status: str
    presence: Optional[bool]

    __table_args__ = (
        UniqueConstraint("student_id", "session_id"),
    )
