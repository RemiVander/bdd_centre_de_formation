from app.models.user import User
from datetime import date
from sqlmodel import Field

class Admin(User, table=True):
    __tablename__ = "admin"
    hiring_date: date = Field()
