
#! core/config.py — Gestion des variables d'environnement
"""
Ce que ça fait :
=>  Ce fichier sert à charger la configuration de l'application, notamment les infos sensibles 
    (mot de passe, URL de la base de données…).
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_DB: str
    PASSWORD: str
    HOST: str
    PORT: int
    DATABASE: str

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.USER_DB}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    class Config:
        env_file = ".env"

settings = Settings()
        
"""
Pourquoi on l'utilise pour DATABASE_URL ?

Dans le code :

@property
def DATABASE_URL(self):
    return f"postgresql://{self.USER_DB}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


Au lieu de stocker DATABASE_URL directement dans le .env, on la construit dynamiquement à partir des autres variables 
(USER_DB, PASSWORD, etc.).
Grâce à @property, tu peux y accéder comme un attribut :

settings.DATABASE_URL  # pas besoin de settings.DATABASE_URL()


Avantages :

Tu n'as pas à mettre à jour l'URL complète dans le .env.
Si tu changes ton utilisateur ou mot de passe, l'URL s'adapte automatiquement.
Le code reste propre et facile à lire.
"""