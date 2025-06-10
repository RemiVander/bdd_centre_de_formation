from sqlmodel import SQLModel, Field

class Equipments(SQLModel, table = True):
    
    __tablename__ = "equipments"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    description : str



computer_lab_equipment = [
    {"name": "Desktop Computer, laptop, monitor, keyboard, mouse", "description": "A stationary computer for general use."},
    {"name": "Desktop Computer, table, ventilo, tv, mouse", "description": "A stationary computer for general use."},
    {"name": "TV, table, ventilo, laptop, mouse", "description": "A stationary computer for general use."},
    {"name": "Projector, Scanner, ventilo, laptop, mouse", "description": "A stationary computer for general use."},
    {"name": ", Scanner, ventilo, laptop, keyboard", "description": "A stationary computer for general use."},

]