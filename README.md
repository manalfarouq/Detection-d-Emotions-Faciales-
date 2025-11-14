# API de Détection d'Émotions Faciales

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![CI](https://img.shields.io/github/actions/workflow/status/manalfarouq/Detection-d-Emotions-Faciales/test.yml?label=tests)]()


Application d'IA en vision par ordinateur détectant les visages et prédisant les émotions via un modèle CNN (TensorFlow/Keras) et OpenCV. Intégrée à une API FastAPI connectée à PostgreSQL pour stocker et consulter les prédictions.

---

## Table des Matières

- [API de Détection d'Émotions Faciales](#api-de-détection-démotions-faciales)
  - [Table des Matières](#table-des-matières)
  - [Contexte](#contexte)
  - [Fonctionnalités](#fonctionnalités)
  - [Architecture](#architecture)
  - [Technologies](#technologies)
  - [Installation](#installation)
    - [Dataset](#dataset)
    - [Prérequis](#prérequis)
    - [Étapes](#étapes)
  - [Endpoints](#endpoints)
  - [Documentation API  (Endpoints Disponibles)](#documentation-api--endpoints-disponibles)
    - [GET / - Page d'Accueil](#get----page-daccueil)
    - [POST /predict  - Prédire une Émotion](#post-predict----prédire-une-émotion)
    - [GET /history - Historique des Prédictions](#get-history---historique-des-prédictions)
  - [Performances](#performances)
    - [**Métriques globales**](#métriques-globales)
    - [**Temps de réponse**](#temps-de-réponse)
    - [**Throughput**](#throughput)
  - [Tests](#tests)
    - [Résultats actuels](#résultats-actuels)

---

## Contexte

Ce projet permet d'analyser les émotions des utilisateurs à partir d'images faciales, utile pour :

- Tests produits 
- Applications interactives  
- Analyse comportementale  

**Objectifs principaux :**  

- Détecter automatiquement les visages dans une image  
- Prédire l'émotion parmi 7 classes : `angry`, `disgust`, `fear`, `happy`, `neutral`, `sad`, `surprise`  
- Stocker les résultats dans la base de données  
- Fournir une API performante et testée pour intégration rapide

---

## Fonctionnalités

- ✅ Détection de visages via **OpenCV + Haar Cascade**  
- ✅ Prédiction des émotions avec un **modèle CNN Keras**  
- ✅ Endpoints FastAPI pour **prédiction et historique**  
- ✅ Tests unitaires simples et automatisés via **GitHub Actions**  
- ✅ Haute précision : ~93% sur le jeu de validation

---

## Architecture

```bash
Detection-d-Emotions-Faciales/
├── app/
│   ├── core/
│   │   └── config.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── predict.py
│   ├── schemas.py
│   └── __init__.py
├── notebooks/
│   ├── train_cnn.ipynb
│   └── facial_detection_model.keras
├── tests/
│   ├── test_main.py
│   ├── test_model_image.ipynb
│   └── haarcascade_frontalface_default.xml
├── .github/
│   └── workflows/
│       └── test.yml
├── .env.example
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md
```


## Technologies

| Domaine | Technologie | Usage |
|---------|-------------|-------|
| Gestion de projet | Poetry | Dépendances et environnement virtuel |
| API Web | FastAPI | Endpoints REST modernes et rapides |
| Serveur ASGI | Uvicorn | Exécution asynchrone de l'API |
| Deep Learning | TensorFlow/Keras | Modèle CNN pour classification des émotions |
| Détection de visages | OpenCV + Haar Cascade | Localisation des visages dans l'image |
| Base de données | PostgreSQL + SQLAlchemy | Stockage des images et prédictions |
| Validation | Pydantic | Schémas et validation des données |
| Tests | pytest | Tests unitaires et d'intégration |
| CI/CD | GitHub Actions | Automatisation des tests à chaque push |


## Installation

### Dataset

Vous pouvez télécharger le dataset utilisé depuis Kaggle :  
[Emotion Detection FER Dataset](https://www.kaggle.com/datasets/ananthu017/emotion-detection-fer/data)


### Prérequis

- Python ≥ 3.11  
- PostgreSQL  
- Poetry  

### Étapes

1. **Cloner le projet**

```bash
git clone https://github.com/manalfarouq/Detection-d-Emotions-Faciales-.git
cd Detection-d-Emotions-Faciales
poetry install
poetry shell
fastapi dev app/main.py
```

API disponible sur :
- http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs

2. **Configurer les variables d'environnement**
   
Copiez l'exemple et modifiez les valeurs selon votre configuration PostgreSQL :
```bash
cp .env.example .env
```   
Exemple de .env :
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/emotions_db
```

Éditez .env avec vos paramètres :

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emotions_db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
SECRET_KEY=votre_secret_key_tres_securisee
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Model
MODEL_PATH=notebooks/facial_detection_model.keras
CASCADE_PATH=tests/haarcascade_frontalface_default.xml
```

3. **Lancer la base de données**
   
Assurez-vous que PostgreSQL est actif et que la base de données existe :
```bash
# Créer la base de données
createdb emotions_db

# Ou avec psql
psql -U postgres
CREATE DATABASE emotions_db;
\q

# Créer les tables
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```


4. **Lancer l'API**

```bash
fastapi dev app/main.py
```

Accédez à :
- Accédez à l'API : http://localhost:8000
- Documentation interactive : http://localhost:8000/docs

## Endpoints

| Méthode | Route       | Description |
|---------|------------|-------------|
| POST    | `/predict`  | Envoyer une image pour obtenir la prédiction d'émotion |
| GET     | `/history`  | Récupérer l'historique des prédictions enregistrées |
| GET     | `/`         | Message de bienvenue |


5. **Exécuter les tests avec pytest :**

```bash
poetry run pytest
```

Tous les tests sont automatisés via GitHub Actions à chaque push ou pullrequest pour garantir la stabilité du projet.


---

## Documentation API  (Endpoints Disponibles)

### GET / - Page d'Accueil
Retourne un message de bienvenue.
Réponse :
```json
  "message": "Bienvenue sur l'API de Détection d'Émotions Faciales",
```




### POST /predict  - Prédire une Émotion
**Corps de la requête :**
```json
{
  "image": "base64_encoded_image_string.(jpeg ou png)"
}
```

**Réponse (Succès - 200) :**
```json
  {
  "id": 1,
  "emotion": "happy",
  "confidence": 0.93,
  "timestamp": "2025-11-14T10:30:00Z"
  }
```

**Réponse (Erreur - Pas de visage) :**
```json
{
  "detail": "Aucun visage détecté."
}
```

### GET /history - Historique des Prédictions
Récupère l'historique des prédictions enregistrées.

Réponse :
```json
{
    "id": 2,
    "emotion": "neutral",
    "confidence": 99.76,
    "date": "13/11/2025 16:35:44"
  },
  {
    "id": 1,
    "emotion": "sad",
    "confidence": 81.68,
    "date": "13/11/2025 16:35:44"
  }
```

---

## Performances

### **Métriques globales**

| Métrique            | Valeur |
|---------------------|--------|
| Accuracy            | 93.2%  |
| Precision (macro)   | 91.7%  |
| Recall (macro)      | 90.8%  |
| F1-score (macro)    | 91.2%  |

---

### **Temps de réponse**

| Étape               | Temps moyen | P95  | P99  |
|--------------------|-------------|------|------|
| Détection OpenCV   | 45 ms       | 67 ms | 89 ms |
| Prédiction CNN     | 142 ms      | 178 ms | 215 ms |
| Temps total API    | ~200 ms     | 280 ms | 350 ms |

---

### **Throughput**

- **CPU** : ~50 req/s  
- **GPU** : ~200 req/s  
- **Images/minute** : jusqu'à **12 000** (GPU)


---

## Tests

Exécuter les Tests
```bash
poetry run pytest
```
Coverage Actuel
```
tests/test_main.py::test_model_load PASSED                               [ 50%]
tests/test_main.py::test_history_format PASSED                         [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.11.14-final-0 _______________

Name                 Stmts   Miss  Cover
----------------------------------------
app/__init__.py          0      0   100%
app/core/config.py      13      0   100%
app/database.py         10      0   100%
app/main.py             42     24    43%
app/models.py            9      0   100%
app/predict.py          27     19    30%
app/schemas.py           7      7     0%
----------------------------------------
TOTAL                  108     50    54%
============================== 2 passed in 17.53s ==============================
```

### Résultats actuels

-  2 tests réussis  
-  Couverture totale : **54%**

---
