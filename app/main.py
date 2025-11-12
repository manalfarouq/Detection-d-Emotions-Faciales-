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


@app.post("/predict_emotion", response_model=PredictionOut)
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

        print(f"Emotion prédite : {predicted_emotion} ({confidence:.2f})")
        return db_pred

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)