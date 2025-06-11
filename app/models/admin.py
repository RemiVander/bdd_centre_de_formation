from app.models.user import User
from datetime import date
from sqlmodel import Field

class Admin(User, table=True):
    """
    Représente un administrateur dans le système, héritant des attributs de la classe User.

    Cette classe étend la classe User pour inclure des attributs spécifiques aux administrateurs,
    tels que la date d'embauche. Elle utilise SQLModel pour la définition des champs.

    Attributes:
        hiring_date (date): La date à laquelle l'administrateur a été embauché.
    """
    __tablename__ = "admin"
    hiring_date: date = Field()
