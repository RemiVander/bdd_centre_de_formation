from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime


class User(SQLModel, table=False):
    """
    Représente un utilisateur dans le système.

    Cette classe définit la structure d'un utilisateur avec des attributs tels que l'identifiant,
    le nom, le prénom, l'adresse e-mail, la date de création, l'état actif et le rôle.
    Elle utilise SQLModel pour la définition des champs et Pydantic pour la validation des types.

    Attributes:
        id (int | None): L'identifiant unique de l'utilisateur. Par défaut, None.
            Cet attribut est la clé primaire.
        name (str): Le nom de l'utilisateur. Doit avoir une longueur maximale de 50 caractères.
        surname (str): Le prénom de l'utilisateur. Doit avoir une longueur maximale de 50 caractères.
        email (EmailStr): L'adresse e-mail de l'utilisateur, validée par Pydantic pour s'assurer
            qu'elle est bien formée.
        creation_date (datetime): La date et l'heure de création de l'utilisateur.
            Par défaut, la date et l'heure actuelles en UTC.
        is_active (bool): Indique si l'utilisateur est actif. Par défaut, True.
        role (str): Le rôle de l'utilisateur dans le système.
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    creation_date: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
    role: str
