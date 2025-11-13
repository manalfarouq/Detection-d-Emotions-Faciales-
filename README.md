# API de Détection d'Émotions Faciales

<p align="left">
  <a href="https://www.python.org" target="_blank" rel="noreferrer">
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python" />
  </a>
  <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer">
    <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI" />
  </a>
  <a href="https://www.tensorflow.org/" target="_blank" rel="noreferrer">
    <img src="https://img.shields.io/badge/TensorFlow-2.x-orange.svg" alt="TensorFlow" />
  </a>
</p>


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
```

2. **Installer les dépendances**

Avec **Poetry** :

```bash
poetry install
```

3. **Configurer les variables d'environnement**
   
Copiez l'exemple et modifiez les valeurs selon votre configuration PostgreSQL :
```bash
cp .env.example .env
```   
Exemple de .env :
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/emotions_db
```

4. **Lancer la base de données**
   
Assurez-vous que PostgreSQL est actif et que la base de données existe :
```bash
createdb emotions_db
```

5. **Créer les tables**

```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

6. **Lancer l'API**

```bash
uvicorn app.main:app --reload
```

## Endpoints

| Méthode | Route       | Description |
|---------|------------|-------------|
| POST    | `/predict`  | Envoyer une image pour obtenir la prédiction d'émotion |
| GET     | `/history`  | Récupérer l'historique des prédictions enregistrées |
| GET     | `/`         | Message de bienvenue |


7. **Exécuter les tests avec pytest :**

```bash
pytest tests/
```

Tous les tests sont automatisés via GitHub Actions à chaque push pour garantir la stabilité du projet.


---


⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile sur GitHub !
