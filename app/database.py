
#* Ce fichier gère la connexion à la base de données

#! Etape 3 ---- Créer la base de données ----
# === SQLAlchemy === permet d'écrire du code Python au lieu de requêtes SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


#* Récupère l'URL de la base de données depuis les paramètres
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL    #? engine = moteur de communication entre ton code et la base

#* Crée le moteur de la base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#* Crée une session locale pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#* Dépendance pour obtenir une session de base de données (Connexion à la base de données)
def get_db():
    db = SessionLocal()   #? ouvre la connexion à la base de données
    try:
        yield db          #? donne la connexion à l'API pour exécuter une action (yield la donne temporairement à FastAPI)
    finally:
        db.close()        #? ferme la connexion à la base de données une fois l'action terminée
        
# FastAPI utilise Depends(get_db) pour accéder à la base sans la laisser ouverte        