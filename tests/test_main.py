from fastapi.testclient import TestClient
from app.main import app
from tensorflow.keras.models import load_model

client = TestClient(app)

def test_model_load():
    model = load_model("notebooks/facial_detection_model.keras")
    assert model is not None
    
    
"""
Ici on importe TestClient de FastAPI.
Tu crées un client de test pour l'app FastAPI.
Cela te permet d'envoyer des requêtes HTTP à ton API comme si tu étais un vrai utilisateur.
"""

def test_history_format():
    r = client.get("/history")            #? Envoyer une requête GET à l'endpoint /history | r contient la réponse de ton endpoint.
    assert r.status_code == 200, f"Status code incorrect: {r.status_code}"
    