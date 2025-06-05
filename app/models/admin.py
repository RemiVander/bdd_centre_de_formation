from app.models.user import User
from datetime import date

class Admin(User, table=True):
    __tablename__ = "admin"
    hiring_date: date 
