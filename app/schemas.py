from pydantic import BaseModel

#* Schéma pour créer une nouvelle prédiction (input)
#* utilisé pour valider et insérer les données reçues par /predict_emotion dans la base de données
class PredictionCreate(BaseModel):
    image_filename: str       # nom ou path de l'image uploadée
    predicted_emotion: str    # résultat du modèle
    confidence: float         # score de confiance (0.0 à 1.0)

#* Schéma pour retourner une prédiction
#* PredictionOut:utilisé pour renvoyer les prédictions (par exemple pour /history)
class PredictionOut(BaseModel):
    id: int
    image_filename: str
    predicted_emotion: str
    confidence: float

    model_config = {"from_attributes": True}  # remplace orm_mode
