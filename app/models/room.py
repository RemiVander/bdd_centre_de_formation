from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy.dialects.postgresql import JSON

class Room(SQLModel, table = True):
    """
    Représente une salle dans le système.

    Cette classe définit la structure d'une salle avec des attributs tels que l'identifiant,
    le nom, la capacité, la localisation, l'état actif et l'identifiant de l'équipement associé.
    Elle utilise SQLModel pour la définition des champs et des contraintes de base de données.

    Attributes:
        id (int | None): L'identifiant unique de la salle. Par défaut, None.
            Cet attribut est la clé primaire.
        name (str): Le nom de la salle. Doit être unique et est indexé pour des recherches rapides.
        capacite (int): La capacité maximale de la salle. Doit être supérieure à zéro.
        localization (str): La localisation de la salle, décrivant son emplacement physique.
        is_active (bool): Indique si la salle est active et disponible pour une utilisation.
            Par défaut, True.
        equipment_id (Optional[int]): L'identifiant de l'équipement associé à la salle.
            Cet attribut est une clé étrangère faisant référence à l'identifiant dans la table des équipements.
    """
    __tablename__ = "room"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    capacite : int = Field(gt=0)
    localization : str
    is_active : bool = True
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipments.id")



