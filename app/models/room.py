from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy.dialects.postgresql import JSON

class Room(SQLModel, table = True):
    __tablename__ = "room"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    capacite : int = Field(gt=0)
    localization : str
    is_active : bool = True
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipments.id")

class Equipments(SQLModel, table = True):
    __tablename__ = "equipments"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    description : str

