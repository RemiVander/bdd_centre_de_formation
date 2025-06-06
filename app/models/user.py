from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy.sql import func


class User(SQLModel, table = False):
    id : int | None = Field(default=None, primary_key=True)
    name: str
    surname : str
    email: str
    creation_date : datetime = Field(default_factory=datetime.utcnow)
    is_active : bool
    role : str