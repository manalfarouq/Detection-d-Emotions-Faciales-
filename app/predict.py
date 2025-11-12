import tensorflow as tf
import numpy as np
import cv2

# Charger le modèle CNN
model = tf.keras.models.load_model("notebooks/facial_detection_model.keras") 

# Liste des classes d'émotions (à adapter selon ton modèle)
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

face_cascade = cv2.CascadeClassifier("tests/haarcascade_frontalface_default.xml")

def predict_emotion(face_img):
    # Redimensionner à la taille attendue par le modèle
    img = cv2.resize(face_img, (48, 48))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    img = img / 255.0                             # normalisation
    img = np.expand_dims(img, axis=(0, -1))       # shape:(batch_size, width, height, channels) -> (1, 48, 48, 1)

    predictions = model.predict(img, verbose=0) 
    
    # Extraire l'index et la confiance
    predictions = predictions[0]
    class_idx = np.argmax(predictions)
    confidence = float(predictions[class_idx])

    return {"emotion": EMOTIONS[class_idx], "confidence": confidence}

def detect_faces(gray_img):
    return face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))