# # Imports
# import shutil
# import uuid
# import cv2
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import img_to_array
# from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db, engine
# from app.models import Base, Prediction
# from app.schemas import PredictionOut
# import os

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil, uuid, os
import cv2

from app.database import get_db, engine
from app.models import Base, Prediction
from app.schemas import PredictionOut
from app.predict import predict_emotion, detect_faces

# # Charger le modèle et les classes
# model = load_model('notebooks/facial_detection_model.keras')
# class_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# # Charger le détecteur de visages
# face_cascade = cv2.CascadeClassifier("tests/haarcascade_frontalface_default.xml")
# if face_cascade.empty():
#     raise IOError("Le fichier haarcascade_frontalface_default.xml n'est pas chargé.")

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
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

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray)
        if len(faces) == 0:
            raise HTTPException(status_code=404, detail="Aucun visage détecté.")

        results = []
        for (x, y, w, h) in faces:
            face_roi = img[y:y+h, x:x+w]
            prediction = predict_emotion(face_roi)
            results.append({
                "label": prediction["emotion"],
                "confidence": prediction["confidence"],
                "box": (int(x), int(y), int(w), int(h))
            })

        first_pred = results[0]
        db_pred = Prediction(image_filename=temp_filename, predicted_emotion=first_pred["label"], confidence=first_pred["confidence"])
        db.add(db_pred)
        db.commit()
        db.refresh(db_pred)
        return db_pred

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)