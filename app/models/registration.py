from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import UniqueConstraint

class Registration(SQLModel, table=True):
    """
    Représente une inscription d'un étudiant à une session de cours dans le système.

    Cette classe définit la structure d'une inscription avec des attributs tels que l'identifiant,
    l'identifiant de l'étudiant, l'identifiant de la session, la date d'inscription, le statut
    de l'inscription et la présence de l'étudiant. Elle utilise SQLModel pour la définition des champs
    et des contraintes de base de données.

    Attributes:
        id (int | None): L'identifiant unique de l'inscription. Par défaut, None.
            Cet attribut est la clé primaire.
        student_id (int): L'identifiant de l'étudiant inscrit. Cet attribut est une clé étrangère
            faisant référence à l'identifiant dans la table des étudiants.
        session_id (int): L'identifiant de la session à laquelle l'étudiant est inscrit.
            Cet attribut est une clé étrangère faisant référence à l'identifiant dans la table des sessions.
        registration_date (datetime): La date et l'heure de l'inscription.
            Par défaut, la date et l'heure actuelles en UTC.
        registration_status (str): Le statut de l'inscription, par exemple, "confirmé" ou "annulé".
        presence (Optional[bool]): Indique si l'étudiant était présent à la session. Peut être None.

    Table Args:
        UniqueConstraint: Une contrainte unique sur les combinaisons de `student_id` et `session_id`
            pour s'assurer qu'un étudiant ne peut s'inscrire qu'une seule fois à une session donnée.
    """
    __tablename__ = "registration"

    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    session_id: int = Field(foreign_key="class_session.id")
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    registration_status: str
    presence: Optional[bool]

    __table_args__ = (
        UniqueConstraint("student_id", "session_id"),
    )
