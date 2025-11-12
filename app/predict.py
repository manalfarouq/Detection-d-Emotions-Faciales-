import tensorflow as tf
import numpy as np
import cv2

# Charger le modèle CNN
model = tf.keras.models.load_model("notebooks/facial_detection_model.keras") 

# Liste des classes d'émotions
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Charger le détecteur de visages
face_cascade = cv2.CascadeClassifier("tests/haarcascade_frontalface_default.xml")

def detect_faces(gray_img):
    return face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

def predict_emotion(image_path):
    # Lire l'image depuis le chemin
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray)
    
    if len(faces) == 0:
        return None, None

    # Prendre le premier visage détecté
    (x, y, w, h) = faces[0]
    face_img = img[y:y+h, x:x+w]

    # Redimensionner et préparer pour le modèle
    face_img = cv2.resize(face_img, (48, 48))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    face_img = face_img / 255.0
    face_img = np.expand_dims(face_img, axis=(0, -1))  # (1, 48, 48, 1)

    preds = model.predict(face_img, verbose=0)[0]
    class_idx = np.argmax(preds)
    confidence = round(float(preds[class_idx]) * 100, 2)
    emotion_label = EMOTIONS[class_idx]

    return confidence, emotion_label