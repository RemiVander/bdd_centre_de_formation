from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime


class User(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    creation_date: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    role: str
