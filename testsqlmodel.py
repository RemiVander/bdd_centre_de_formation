from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, func
from faker import Faker


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


fake = Faker()
engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

# Fonction pour générer des données fictives et les insérer dans la base de données
def populate_heroes_table(num_heroes: int = 10):
    with Session(engine) as session:
        for _ in range(num_heroes):
            hero = Hero(
                name=fake.unique.first_name(),
                secret_name=fake.unique.user_name(),
                age=fake.random_int(min=18, max=80)
            )
            session.add(hero)
        session.commit()

# Appeler la fonction pour peupler la table avec 10 héros fictifs
populate_heroes_table(10)




# with Session(engine) as session:
#     statement = delete(Hero).where(Hero.name == "Spider-Boy")
#     result = session.exec(statement)
#     session.commit()

# # Suppression des doublons
# with Session(engine) as session:
#     # Sous-requête pour obtenir les IDs des doublons
#     subquery = (
#         select(
#             Hero.name,
#             Hero.secret_name,
#             func.min(Hero.id).label("min_id")
#         )
#         .group_by(Hero.name, Hero.secret_name)
#         .having(func.count(Hero.id) > 1)
#         .subquery()
#     )

#     # Requête pour obtenir les IDs des doublons à supprimer
#     duplicate_ids = session.exec(
#         select(Hero.id)
#         .join(
#             subquery,
#             (Hero.name == subquery.c.name) &
#             (Hero.secret_name == subquery.c.secret_name) &
#             (Hero.id != subquery.c.min_id)
#         )
#     ).scalars().all()

#     # Supprimer les doublons
#     for duplicate_id in duplicate_ids:
#         hero_to_delete = session.get(Hero, duplicate_id)
#         if hero_to_delete:
#             session.delete(hero_to_delete)

#     session.commit()