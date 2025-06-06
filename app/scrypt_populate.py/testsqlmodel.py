import sys, os
sys.path.append(os.getcwd())
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, func
from faker import Faker
import random
from app.models.teacher import Teacher
from app.models.room import Room
from app.models.class_session import ClassSession, Status, Requirement
from app.models.student import Student
from app.models.admin import Admin
from app.models.equipments import Equipments, computer_lab_equipment
from datetime import date, timedelta, datetime
from app.database import engine

SQLModel.metadata.create_all(engine)
fake = Faker(locale="fr_FR")

# Fonctions de nettoyage
def clear_all_data():
    """Nettoie toutes les données existantes"""
    with Session(engine) as session:
        # Ordre important à cause des clés étrangères
        session.exec(delete(ClassSession))
        session.exec(delete(Teacher))
        session.exec(delete(Room))
        session.exec(delete(Student))
        session.exec(delete(Admin))
        session.exec(delete(Requirement))
        session.exec(delete(Status))
        session.exec(delete(Equipments))
        session.commit()
        print("Toutes les données ont été nettoyées.")

def clear_specific_table(table_class):
    """Nettoie une table spécifique"""
    with Session(engine) as session:
        session.exec(delete(table_class))
        session.commit()
        print(f"Table {table_class.__name__} nettoyée.")

# Fonction pour générer des données fictives teacher et les insérer dans la base de données
def populate_table_teacher(num_teacher: int = 10):
    with Session(engine) as session:
        # Vérifier si des teachers existent déjà
        existing_count = session.exec(select(func.count(Teacher.id))).first()
        if existing_count > 0:
            print(f"Attention: {existing_count} enseignants existent déjà. Nettoyage recommandé.")
        
        for i in range(num_teacher):
            # Utiliser un nom unique avec un index pour éviter les doublons
            teacher = Teacher(
                name=f"{fake.first_name()}",  # Ajout d'un index pour l'unicité
                surname=fake.user_name(),  # Ajout d'un index pour l'unicité
                age=fake.random_int(min=25, max=65),
                email=f"teacher_{i}_{fake.email()}",  # Email unique
                is_active=True,
                role="teacher",
                speciality=random.choice(["Data Science", "Web Development", "Machine Learning", "Database", "DevOps"]),
                hiring_date=fake.date_between(start_date='-5y', end_date='today'),
                hours_rate=random.choice([45.0, 50.0, 55.0, 60.0, 65.0, 70.0]),
                bio=fake.job()
            )
            session.add(teacher)
        session.commit()
        print(f"{num_teacher} enseignants créés avec succès.")

# Fonction pour générer des salles fictives et les insérer dans la base de données
def populate_table_room(num_room: int = 10):
    room_names = [
        "Salle Alpha", "Salle Beta", "Salle Gamma", "Salle Delta", 
        "Salle Epsilon", "Salle Zeta", "Salle Eta", "Salle Theta",
        "Lab Python", "Lab Data", "Salle Conférence", "Salle Projet",
        "Amphithéâtre", "Salle TP", "Salle Formation"
    ]
    
    with Session(engine) as session:
        existing_count = session.exec(select(func.count(Room.id))).first()
        if existing_count > 0:
            print(f"Attention: {existing_count} salles existent déjà. Nettoyage recommandé.")
        
        for i in range(min(num_room, len(room_names))):
            room = Room(
                name=room_names[i],  # Noms prédéfinis pour éviter les doublons
                capacite=random.choice([8, 12, 16, 20, 24, 30]),
                localization=f"Étage {random.randint(1, 3)}, {fake.street_address()}",
                is_active=True,
                role="user"  # Si ce champ existe dans votre modèle
            )
            session.add(room)
        session.commit()
        print(f"{min(num_room, len(room_names))} salles créées avec succès.")

# Fonction pour générer des requirements
def populate_table_requirements(num_requirements: int = 10):
    requirements_list = [
        "Connaissance Python", "Bases SQL", "Mathématiques niveau bac",
        "Statistiques descriptives", "Logique algorithmique", "Excel avancé",
        "Anglais technique", "Bases de données", "Git/GitHub", "Linux basics"
    ]
    
    with Session(engine) as session:
        existing_count = session.exec(select(func.count(Requirement.id))).first()
        if existing_count > 0:
            print(f"Attention: {existing_count} prérequis existent déjà. Nettoyage recommandé.")
        
        for i, req_name in enumerate(requirements_list[:num_requirements]):
            requirement_entry = Requirement(
                name=req_name
            )
            session.add(requirement_entry)
        session.commit()
        print(f"{min(num_requirements, len(requirements_list))} prérequis créés avec succès.")

# Fonction pour générer les status 
def populate_table_status():
    with Session(engine) as session:
        # Vérifier si les status existent déjà
        existing_statuses = session.exec(select(Status)).all()
        if existing_statuses:
            print(f"Status déjà existants: {[s.type for s in existing_statuses]}")
            return
        
        statuses = ['OPEN', 'ARCHIVED', 'CLOSED']
        for status_type in statuses:
            st = Status(type=status_type)
            session.add(st)
        session.commit()
        print("Status créés avec succès.")

# Fonction pour générer des sessions fictives avec des horaires réalistes
def populate_realistic_class_sessions(num_weeks: int = 4):
    """Génère des sessions avec des horaires plus réalistes"""
    with Session(engine) as session:
        teachers = session.exec(select(Teacher)).all()
        rooms = session.exec(select(Room)).all()
        statuses = session.exec(select(Status)).all()
        requirements = session.exec(select(Requirement)).all()
        
        if not all([teachers, rooms, statuses, requirements]):
            print("Erreur: Il manque des données de base (teachers, rooms, statuses, ou requirements)")
            return

        # Horaires types de cours
        time_slots = [
            (8, 0, 2),    # 8h-10h
            (10, 15, 2),  # 10h15-12h15
            (13, 30, 1.5), # 13h30-15h
            (15, 15, 2),  # 15h15-17h15
        ]
        
        course_titles = [
            "Introduction à Python",
            "Bases de données relationnelles", 
            "Machine Learning fondamental",
            "Analyse de données avec Pandas",
            "Visualisation des données",
            "Statistiques descriptives",
            "Programmation orientée objet",
            "API REST avec FastAPI",
            "Docker et conteneurisation",
            "Git et versioning"
        ]

        # Générer des sessions pour les prochaines semaines
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        sessions_created = 0
        
        for week in range(num_weeks):
            # Pour chaque jour de la semaine (lundi à vendredi)
            for day in range(5):
                current_date = base_date + timedelta(weeks=week, days=day)
                
                # Générer 2-4 cours par jour
                num_sessions_day = random.randint(2, 4)
                used_time_slots = []
                used_rooms = []
                
                for _ in range(num_sessions_day):
                    # Éviter les conflits de salles et d'horaires
                    available_slots = [slot for slot in time_slots if slot not in used_time_slots]
                    available_rooms = [room for room in rooms if room not in used_rooms]
                    
                    if not available_slots or not available_rooms:
                        break
                    
                    time_slot = random.choice(available_slots)
                    room = random.choice(available_rooms)
                    teacher = random.choice(teachers)
                    status = random.choice(statuses)
                    requirement = random.choice(requirements)
                    
                    start_time = current_date.replace(hour=time_slot[0], minute=time_slot[1])
                    end_time = start_time + timedelta(hours=time_slot[2])
                    
                    cs = ClassSession(
                        title=random.choice(course_titles),
                        description=fake.sentence(),
                        start_date=start_time,
                        end_date=end_time,
                        max_capacity=random.randint(5, room.capacite),
                        statut_id=status.id,
                        room_id=room.id,
                        teacher_id=teacher.id,
                        requirement_id=requirement.id
                    )
                    
                    session.add(cs)
                    used_time_slots.append(time_slot)
                    used_rooms.append(room)
                    sessions_created += 1
        
        session.commit()
        print(f"{sessions_created} sessions créées avec succès pour {num_weeks} semaines")

# Fonction pour générer des étudiants fictifs et les insérer dans la base de données
def populate_table_student(num_student: int = 20):
    diploma_list = ["Data Engineer", "Data Scientist", "Data Analyst", "DevOps"]
    with Session(engine) as session:
        existing_count = session.exec(select(func.count(Student.id))).first()
        if existing_count > 0:
            print(f"Attention: {existing_count} étudiants existent déjà.")
        
        for i in range(num_student):
            student = Student(
                name=f"{fake.first_name()}_{i}",
                surname=f"{fake.last_name()}_{i}",
                email=f"student_{i}_{fake.email()}",
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=30),
                level_degree=random.randint(1, 7),
                telephone=random.randint(1000000000, 9999999999),  # Numéro plus réaliste
                registration_date=fake.date_between(start_date='-2y', end_date='today'),
                diploma=random.choice(diploma_list),
                is_active=fake.boolean(),
                role="student"
            )
            session.add(student)
        session.commit()
        print(f"{num_student} étudiants créés avec succès.")

# Fonction pour générer des admins fictifs et les insérer dans la base de données
def populate_table_admin(num_admin: int = 2):
    with Session(engine) as session:
        existing_count = session.exec(select(func.count(Admin.id))).first()
        if existing_count > 0:
            print(f"Attention: {existing_count} admins existent déjà.")
        
        for i in range(num_admin):
            admin = Admin(
                name=f"{fake.first_name()}_{i}",
                surname=f"{fake.last_name()}_{i}",
                email=f"admin_{i}_{fake.email()}",
                hiring_date=fake.date_between(start_date='-3y', end_date='today'),
                is_active=fake.boolean(),
                role="admin"
            )
            session.add(admin)
        session.commit()
        print(f"{num_admin} admins créés avec succès.")

# Fonction pour générer des equipements fictifs et les insérer dans la base de données
def populate_table_equipments():
    with Session(engine) as session:
        existing_count = session.exec(select(func.count(Equipments.id))).first()
        if existing_count > 0:
            print(f"Attention: {existing_count} équipements existent déjà.")
            return
        
        for equipment in computer_lab_equipment:
            equipment_entry = Equipments(
                name=equipment["name"],
                description=equipment["description"]
            )
            session.add(equipment_entry)
        session.commit()
        print("Équipements créés avec succès.")

if __name__ == "__main__":
    print("=== DÉBUT DU PEUPLEMENT DE LA BASE DE DONNÉES ===")
    
    # Option 1: Nettoyer toutes les données avant de recommencer
    print("\n1. Nettoyage des données existantes...")
    clear_all_data()
    
    # Option 2: Peupler les tables dans l'ordre correct
    print("\n2. Création des données de base...")
    populate_table_equipments()
    populate_table_status()
    populate_table_requirements(10)
    populate_table_teacher(10)
    populate_table_room(6)
    populate_table_student(20)
    populate_table_admin(2)
    
    print("\n3. Création des sessions de cours...")
    populate_realistic_class_sessions(4)  # 4 semaines de cours
    
    print("\n=== PEUPLEMENT TERMINÉ AVEC SUCCÈS ===")