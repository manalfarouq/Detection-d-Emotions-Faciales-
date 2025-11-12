#* database.py — Gère la connexion à la base de données
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#* Crée le moteur SQLAlchemy avec l'URL depuis config.py
engine = create_engine(settings.DATABASE_URL)

#* Crée une session locale pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#* Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
