from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base


# Création de la base pour les modèles
Base = declarative_base()

# Modèle pour les émotions
class Prediction(Base):
    __tablename__ = "predictions" 

    id = Column(Integer, primary_key=True, index=True)
    predicted_emotion = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())