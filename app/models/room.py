from sqlmodel import SQLModel, Field
from typing import Dict
from sqlalchemy.dialects.postgresql import JSON

class Room(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    capacite : int = Field(gt=0)
    localization : str
    is_active : bool = True


class Equipments(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)