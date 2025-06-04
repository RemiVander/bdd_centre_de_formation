from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy.sql import func

class User(SQLModel, table = False):
    id : int | None = Field(default=None, primary_key=True)
    name: str
    surname : str
    email: str
    creation_date : datetime = Field(sa_column_kwargs={"server_default": func.now()})
    is_active : bool
    role : str