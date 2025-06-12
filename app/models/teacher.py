from sqlmodel import  Field
from datetime import date
from typing import Optional
from pydantic import model_validator
from app.models.user import User


class Teacher(User, table=True):
    """
    Représente un enseignant dans le système, héritant des attributs de la classe User.

    Cette classe étend la classe User pour inclure des attributs spécifiques aux enseignants,
    tels que la spécialité, la date d'embauche, le taux horaire et une biographie.
    Elle utilise SQLModel pour la définition des champs et Pydantic pour la validation des données.

    Attributes:
        speciality (str): La spécialité de l'enseignant.
        hiring_date (date): La date d'embauche de l'enseignant.
        hours_rate (float): Le taux horaire de l'enseignant, doit être supérieur ou égal à zéro.
        bio (Optional[str]): Une brève biographie de l'enseignant. Peut être None.
    """
    __tablename__ = "teacher"

    speciality: str
    hiring_date: date 
    hours_rate: float = Field(ge=0) 
    bio: Optional[str] = None

    @model_validator(mode='after')
    def check_hiring_date(self):
        """
        Valide que la date d'embauche est antérieure à la date actuelle.

        Cette méthode est appelée après la création d'une instance de Teacher pour s'assurer
        que la date d'embauche est bien une date passée. Si la date d'embauche est postérieure
        ou égale à la date actuelle, une erreur est levée.

        Returns:
            Teacher: L'instance de Teacher validée.

        Raises:
            ValueError: Si la date d'embauche est postérieure ou égale à la date actuelle.
        """
        if self.hiring_date >= date.today():
            raise ValueError("hiring date must be before date today")
        return self
