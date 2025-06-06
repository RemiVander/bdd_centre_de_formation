from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy.sql import func
from pydantic import EmailStr


class User(SQLModel, table = False):
    id : int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    surname : str = Field(max_length=50)
    email: EmailStr
    creation_date : datetime = Field(default_factory=datetime.utcnow)
    is_active : bool
    role : str