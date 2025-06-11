from sqlmodel import Field
from datetime import date, datetime, timezone
from typing import Optional
from pydantic import model_validator
from app.models.user import User


class Student(User, table=True):
    """
    Représente un étudiant dans le système, héritant des attributs de la classe User.

    Cette classe étend la classe User pour inclure des attributs spécifiques aux étudiants,
    tels que la date de naissance, le niveau d'études, le numéro de téléphone, la date d'inscription,
    et le diplôme. Elle utilise SQLModel pour la définition des champs et Pydantic pour la validation des données.

    Attributes:
        birth_date (date): La date de naissance de l'étudiant.
        level_degree (Optional[int]): Le niveau d'études actuel de l'étudiant. Peut être None.
        telephone (Optional[int]): Le numéro de téléphone de l'étudiant. Peut être None.
        registration_date (datetime): La date et l'heure d'inscription de l'étudiant.
            Par défaut, la date et l'heure actuelles en UTC.
        diploma (Optional[str]): Le diplôme obtenu ou visé par l'étudiant. Peut être None.
    """
    __tablename__ = "student"

    birth_date: date 
    level_degree: Optional[int] = None
    telephone: Optional[int] = None
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    diploma: Optional[str] = None

    @model_validator(mode='after')
    def check_legal_age(self):
        """
        Valide que l'étudiant a l'âge légal.

        Cette méthode est appelée après la création d'une instance de Student pour s'assurer
        que l'étudiant a atteint l'âge légal. Si la date de naissance indique que l'étudiant
        est mineur, une erreur est levée.

        Returns:
            Student: L'instance de Student validée.

        Raises:
            ValueError: Si l'étudiant est mineur, c'est-à-dire né après le 1er juin 2009.
        """
        if self.birth_date >= date(2009,6,1):
            raise ValueError("student is underage")
        return self
