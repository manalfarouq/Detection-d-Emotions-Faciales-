from pydantic import BaseModel
from datetime import datetime

#* Schéma pour créer une nouvelle prédiction (input)
#* utilisé pour valider et insérer les données reçues par /predict_emotion dans la base de données
class PredictionCreate(BaseModel):
    predicted_emotion: str    # résultat du modèle
    confidence: float         # score de confiance (0.0 à 1.0)
    created_at: datetime

    model_config = {"from_attributes": True}  # remplace orm_mode
