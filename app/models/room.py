from sqlmodel import SQLModel, Field
from typing import Dict
from sqlalchemy.dialects.postgresql import JSON

class Room(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    capacite : int = Field(gt=0)
    localization : str
    equipments : Dict = Field(sa_type=JSON)
    is_active : bool = True


equipments={"video_projecteur": True, "tableau": "blanc"}