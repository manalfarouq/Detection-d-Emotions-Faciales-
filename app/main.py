from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil, uuid, os, cv2

from app.database import get_db, engine
from app.models import Base, Prediction
from app.schemas import PredictionOut
from app.predict import predict_emotion, detect_faces

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer l'application
app = FastAPI(title="Emotion Detection API")

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de Détection d'Émotions Faciales!"}


@app.post("/predict_emotion")
async def predict_emotion_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ALLOWED_TYPES = ["image/jpeg", "image/png"]
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Type non autorisé: {file.content_type}")

    file_ext = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_ext}"

    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file.file.close()

    try:
        img = cv2.imread(temp_filename)
        if img is None:
            raise HTTPException(status_code=400, detail="Impossible de lire l'image.")

        confidence, predicted_emotion = predict_emotion(temp_filename)
        if confidence is None or predicted_emotion is None:
            raise HTTPException(status_code=404, detail="Aucun visage détecté.")

        db_pred = Prediction(
            image_filename=temp_filename,
            predicted_emotion=predicted_emotion,
            confidence=confidence
        )
        db.add(db_pred)
        db.commit()
        db.refresh(db_pred)

        # Retourner seulement ce qu'on veut afficher
        return {
            "id": db_pred.id,
            "image": db_pred.image_filename,
            "emotion": db_pred.predicted_emotion,
            "confidence": round(db_pred.confidence, 2),
            "date": db_pred.created_at.strftime("%d/%m/%Y %H:%M:%S")  
        }

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    """
    Récupère toutes les prédictions enregistrées dans la base de données
    et les renvoie avec un affichage simple
    """
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).all()
    result = []
    for p in predictions:
        result.append({
            "id": p.id,
            "image": p.image_filename,
            "emotion": p.predicted_emotion,
            "confidence": round(p.confidence, 2),  # arrondi à 2 décimales
            "date": p.created_at.strftime("%d/%m/%Y %H:%M:%S")  # date lisible
        })

    return result          