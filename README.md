# ⚽ CANiQ — Système RAG pour la CAN 2025

## 🎯 Objectif du projet
CANiQ est un système RAG (Retrieval-Augmented Generation) spécialisé dans la Coupe d'Afrique des Nations 2025. Il permet de poser des questions en langage naturel sur la compétition et d'obtenir des réponses précises basées sur un corpus documentaire enrichi.

Composants principaux :
- **Backend Flask** : API REST pour l'indexation, l'upload et l'interrogation
- **Moteur RAG** : Pipeline complet avec embeddings, FAISS et génération de réponses
- **Google Gemini** : LLM pour la génération de réponses contextuelles
- **Frontend Streamlit** : Interface utilisateur moderne avec carte interactive des stades

---

## ⚙️ Stack technique

### 🖧 Backend :
- **Python 3.10+**
- **Flask** – Framework web léger pour exposer les endpoints `/ask` et `/healthcheck`
- **LangChain** – Orchestration du pipeline RAG
- **FAISS** – Moteur de recherche vectorielle
- **SentenceTransformers** – Génération des embeddings
- **Google Generative AI (Gemini API)** – Modèle LLM pour la génération de texte
- **Pydantic** – Validation des modèles de requêtes/réponses

### 💻 Frontend :
- **Streamlit** – Interface utilisateur simple et rapide
- Champ de saisie pour poser des questions
- Affichage de la réponse et des sources documentaires
- Carte interactive des stades

---

## 📂 Structure du projet
```
CANiQ/
├── backend/
│   ├── main.py           # API Flask principale
│   ├── rag_engine.py     # Extraction, nettoyage, embeddings, FAISS, retrieval
│   ├── models.py         # Schémas Pydantic
│   └── requirements.txt
├── frontend/
│   ├── app.py            # Interface Streamlit
│   └── stades_can2025.csv
├── data/
│   └── raw_documents/    # Documents à indexer
├── .env.example          
└── README.md
```

---

## 🛠️ Installation (locale)

1. Cloner le dépôt
```bash
git clone <repo-url>
cd CANiQ
```

2. Créer et activer un virtualenv
- PowerShell (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- cmd (Windows)
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```
- macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances (backend + frontend)
```bash
pip install -r backend/requirements.txt
pip install streamlit requests
```

---

## 🔑 Configuration des clés API
Copier l'exemple de configuration et renseigner les clés nécessaires :
```bash
cp .env.example .env
```
`.env` :
```
GEMINI_API_KEY=Your_Key
API_BASE="http://localhost:8000"
# EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
DATA_DIR="../data/raw_documents"
FAISS_DIR="../data/vector_store"
EMBED_MODEL="all-MiniLM-L6-v2.gguf2.f16.gguf"
CHUNK_SIZE=500
CHUNK_OVERLAP=120
TOP_K=4
UPLOAD_FOLDER="../data/raw_documents"
```
- Ouvrir `.env` et remplacer `Your_Key` par votre clé Gemini personnelle.
  ⚠️ Important — Remplacez Your_Key par votre propre clé Gemini API obtenue sur Google AI Studio.  
Sans cette clé, le modèle de génération ne fonctionnera pas.
---

## 🚀 Démarrage

### Backend (développement)
```bash
cd backend
python main.py
```
- Serveur par défaut : http://localhost:8000
- Endpoint santé : `GET /healthcheck` → renvoie `{"status":"ok"}`

### Frontend (Streamlit)
```bash
cd frontend
streamlit run app.py
```
- Ouvrir l'URL affichée (ex : http://localhost:8501)

---

## 📡 Endpoints principaux

- GET /healthcheck  
  Vérifie l'état du service.

- POST /reindex  
  Reconstruit l'index FAISS depuis `data/raw_documents`.  
  - Mode synchrone (JSON final) : `POST /reindex?stream=false`  
  - Mode stream (SSE) : `POST /reindex` (consommer le flux)

- POST /upload  
  Permet d’uploader un fichier (PDF, DOCX, TXT) avec option de réindexation.  

- POST /ask  
  Poser une question au système RAG.

---

## ⚠️ Notes
- L'indexation peut prendre plusieurs minutes selon le volume et le CPU.  
---

## ✅ Fonctionnalités implémentées
- Extraction texte PDF / DOCX / TXT
- Nettoyage et normalisation texte
- Chunking sémantique
- Embeddings via sentence-transformers (ou wrapper LangChain)
- Indexation FAISS locale (persist)
- Endpoints REST pour ask/upload/reindex
- Frontend Streamlit avec upload, reindex, question/answer UI
- Option Gemini LLM si clé fournie (fallback extractif sinon)
  
---

## 👩‍💻 Auteur
Khadija ZOUHAIR  
Étudiante ingénieure en Informatique & Data Science — ENSA Khouribga

