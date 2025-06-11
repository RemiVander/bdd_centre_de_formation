from sqlmodel import SQLModel, Field

class Equipments(SQLModel, table = True):
    """
    Représente un équipement dans le système.

    Cette classe définit la structure d'un équipement avec des attributs tels que l'identifiant,
    le nom et la description. Elle utilise SQLModel pour la définition des champs et des contraintes
    de base de données.

    Attributes:
        id (int | None): L'identifiant unique de l'équipement. Par défaut, None.
            Cet attribut est la clé primaire.
        name (str): Le nom de l'équipement. Doit être unique et est indexé pour des recherches rapides.
        description (str): Une description détaillée de l'équipement et de son utilisation.
    """

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