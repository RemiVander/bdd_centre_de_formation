from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional
from pydantic import model_validator

class ClassSession(SQLModel, table=True):
    """
    Représente une session de cours dans le système.

    Cette classe définit la structure d'une session de cours avec des attributs tels que l'identifiant,
    le titre, la description, les dates de début et de fin, la capacité maximale, et les identifiants
    des statuts, des prérequis, de la salle et de l'enseignant associés. Elle utilise SQLModel pour
    la définition des champs et des contraintes de base de données.

    Attributes:
        id (int | None): L'identifiant unique de la session de cours. Par défaut, None.
            Cet attribut est la clé primaire.
        title (str): Le titre de la session de cours. Doit avoir une longueur maximale de 100 caractères.
        description (Optional[str]): Une description de la session de cours. Peut être None.
        start_date (datetime): La date et l'heure de début de la session de cours.
        end_date (datetime): La date et l'heure de fin de la session de cours.
        max_capacity (int): La capacité maximale de participants pour la session de cours.
        statut_id (int): L'identifiant du statut de la session. Par défaut, 1, qui correspond à 'OPEN'.
            Cet attribut est une clé étrangère faisant référence à l'identifiant dans la table des statuts.
        requirement_id (Optional[int]): L'identifiant du prérequis pour la session. Peut être None.
            Cet attribut est une clé étrangère faisant référence à l'identifiant dans la table des prérequis.
        room_id (int): L'identifiant de la salle où se déroule la session.
            Cet attribut est une clé étrangère faisant référence à l'identifiant dans la table des salles.
        teacher_id (int): L'identifiant de l'enseignant responsable de la session.
            Cet attribut est une clé étrangère faisant référence à l'identifiant dans la table des enseignants.
    """
    __tablename__ = "class_session"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    max_capacity: int
    statut_id: int = Field(default=1, foreign_key="status.id")  # Supposons que 'OPEN' = id 1 dans status
    requirement_id: Optional[int] = Field(default=None, foreign_key="requirement.id")
    room_id: int = Field(foreign_key="room.id")
    teacher_id: int = Field(foreign_key="teacher.id")

    @model_validator(mode="after")
    def check_dates(self):
        """
        Valide que la date de début est antérieure à la date de fin.

        Cette méthode est appelée après la création d'une instance de ClassSession pour s'assurer
        que la date de début est bien antérieure à la date de fin. Si ce n'est pas le cas, une erreur est levée.

        Returns:
            ClassSession: L'instance de ClassSession validée.

        Raises:
            ValueError: Si la date de début est postérieure ou égale à la date de fin.
        """
        if self.start_date >= self.end_date:
            raise ValueError("start must be before end date")
        return self

    
class Requirement(SQLModel, table = True):
    """
    Représente un prérequis pour une session de cours dans le système.

    Cette classe définit la structure d'un prérequis avec des attributs tels que l'identifiant
    et le nom. Elle utilise SQLModel pour la définition des champs et des contraintes de base de données.

    Attributes:
        id (int | None): L'identifiant unique du prérequis. Par défaut, None.
            Cet attribut est la clé primaire.
        name (str): Le nom du prérequis. Doit être unique.
    """
    __tablename__ = "requirement"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True)

class Status(SQLModel, table = True):
    """
    Représente un statut pour une session de cours dans le système.

    Cette classe définit la structure d'un statut avec des attributs tels que l'identifiant
    et le type. Elle utilise SQLModel pour la définition des champs et des contraintes de base de données.

    Attributes:
        id (int | None): L'identifiant unique du statut. Par défaut, None.
            Cet attribut est la clé primaire.
        type (str): Le type de statut. Doit être unique.
    """
    __tablename__ = "status"
    id : int | None = Field(default=None, primary_key=True)
    type : str = Field(unique=True)
