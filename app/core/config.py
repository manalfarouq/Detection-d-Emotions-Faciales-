
#! core/config.py — Gestion des variables d'environnement
"""
Ce que ça fait :
=>  Ce fichier sert à charger la configuration de l'application, notamment les infos sensibles 
    (mot de passe, URL de la base de données…).
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
