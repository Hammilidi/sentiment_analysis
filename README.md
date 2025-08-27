# 🎯 Sentiment Analysis API

API d'analyse de sentiments utilisant **DistilBERT** pour classifier automatiquement les textes en sentiments positifs ou négatifs avec un score de confiance.

## 🚀 Démos en ligne

**🌐 Application Gradio :** [https://huggingface.co/spaces/Hammilidi/sentiments_analysis](https://huggingface.co/spaces/Hammilidi/sentiments_analysis)

**🐳 Application Docker :** [https://huggingface.co/spaces/Hammilidi/sentiments_analysis_docker](https://huggingface.co/spaces/Hammilidi/sentiments_analysis_docker)

**📦 Repository GitHub :** [https://github.com/Hammilidi/sentiment_analysis](https://github.com/Hammilidi/sentiment_analysis)

**🐋 Image Docker Hub :** [hammilidi/sentiments_analysis](https://hub.docker.com/r/hammilidi/sentiments_analysis)

## ✨ Fonctionnalités

- **Analyse de sentiment** : Classification POSITIVE/NEGATIVE avec score de confiance
- **API REST** complète avec validation des données
- **Interface Gradio** intuitive pour tester l'analyse
- **Interface web** FastAPI avec Swagger UI
- **Documentation automatique** avec Swagger UI
- **Conteneurisé** avec Docker
- **Déployé** sur Hugging Face Spaces (2 versions)
- **Tests unitaires** et benchmark de performance
- **Image Docker** disponible sur Docker Hub

## 🏗️ Architecture

```
sentiment_analysis/
├── app/
│   └── main.py              # API FastAPI principale
├── static/
│   └── index.html           # Interface web de test
├── tests/
│   └── test_api.py          # Tests unitaires
├── gradio/
│   └── app.py               # Interface Gradio
├── Dockerfile               # Configuration Docker
├── requirements.txt         # Dépendances Python
├── benchmark.py            # Script de benchmark
└── README.md               # Documentation
```

## 🛠️ Installation et utilisation

### Option 1: Utiliser l'image Docker Hub (Recommandé)

```bash
# Télécharger et lancer l'image depuis Docker Hub
docker run -p 7860:7860 hammilidi/sentiments_analysis
```

### Option 2: Lancement local avec Docker

```bash
# Cloner le repository
git clone https://github.com/Hammilidi/sentiment_analysis.git
cd sentiment_analysis

# Construire l'image Docker
docker build -t sentiment-api .

# Lancer le container
docker run -p 7860:7860 sentiment-api
```

### Option 3: Lancement avec Uvicorn (API FastAPI)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
cd sentiments_analysis
uvicorn main:app --host 0.0.0.0 --port 7860 --reload
```

### Option 4: Lancement avec Gradio

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'interface Gradio
cd sentiment_analysis/sentiment_analysis/
python app.py
```

### Accès aux applications

- **Interface Gradio** : http://localhost:7860 (version Gradio)
- **API FastAPI** : http://localhost:7860 (version Docker/FastAPI)
- **Documentation API** : http://localhost:7860/docs
- **Health check** : http://localhost:7860/health

## 📡 Utilisation de l'API

### Endpoint principal: POST /predict

**Exemple de requête :**
```bash
curl -X POST "http://localhost:7860/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "This product is amazing!"}'
```

**Réponse FastAPI :**
```json
{
  "sentiment": "POSITIVE",
  "confidence": 0.9998,
  "text": "This product is amazing!",
  "processing_time_ms": 45.2
}
```

**Réponse Gradio (format personnalisé) :**
```json
[
  {
    "text": "This product is amazing!",
    "label": "POSITIVE",
    "score": 0.9998656511306763
  }
]
```

### Autres endpoints (API FastAPI)

- `GET /` - Interface web de test
- `GET /health` - Vérification de l'état de l'API  
- `GET /docs` - Documentation Swagger interactive

## 🧪 Tests et validation

### Lancer les tests unitaires

```bash
# Installation de pytest
pip install pytest

# Exécution des tests
python -m pytest tests/test_api.py -v
```

**Tests couverts :**
- ✅ Health check de l'API
- ✅ Prédiction sentiment positif
- ✅ Prédiction sentiment négatif  
- ✅ Gestion des erreurs (texte vide, trop long)
- ✅ Validation des formats JSON
- ✅ Tests de performance

### Benchmark de performance

```bash
# Lancer le benchmark comparatif
python benchmark.py
```

## 📊 Tests & Benchmark

### Résultats des tests unitaires
- **10 tests** passés avec succès
- **Couverture** : endpoints principaux, validation, gestion d'erreurs
- **Performance** : temps de réponse optimal

### Résultats du benchmark (10 phrases de test)
- **2 modèles** comparés sur CPU
- **Tests identiques** pour comparaison équitable
- **Métriques** : latence moyenne, précision, temps min/max

### Benchmark comparatif

| Modèle | Latence Moyenne | Précision | Min/Max |
|--------|----------------|-----------|---------|
| **distilbert-base-uncased-finetuned-sst-2-english** | **77.7ms** | **100.0%** | 43/217ms |
| cardiffnlp/twitter-roberta-base-sentiment-latest | 178.2ms | 10.0% | 132/376ms |

**🏆 Recommandation :** DistilBERT offre le meilleur équilibre performance/précision avec une latence 2.3x plus rapide et une précision parfaite.

### Cas de test types

| Texte | Sentiment attendu | Résultat DistilBERT |
|-------|------------------|---------------------|
| "This product is absolutely amazing!" | POSITIVE ✅ | POSITIVE (100.0%) |
| "Terrible quality, waste of money!" | NEGATIVE ✅ | NEGATIVE (100.0%) |
| "It's okay, nothing special but works fine." | NEUTRAL ➡️ | POSITIVE (100.0%) |
| "Outstanding customer service!" | POSITIVE ✅ | POSITIVE (100.0%) |
| "Very disappointed with this purchase." | NEGATIVE ✅ | NEGATIVE (100.0%) |

## 🐳 Déploiement

### Hugging Face Spaces

**2 versions déployées :**

1. **Version Gradio** : [https://huggingface.co/spaces/Hammilidi/sentiments_analysis](https://huggingface.co/spaces/Hammilidi/sentiments_analysis)
   - Interface utilisateur simple et intuitive
   - SDK : Gradio
   - Format de réponse personnalisé avec le texte original

2. **Version Docker** : [https://huggingface.co/spaces/Hammilidi/sentiments_analysis_docker](https://huggingface.co/spaces/Hammilidi/sentiments_analysis_docker)
   - API REST complète avec FastAPI
   - SDK : Docker
   - Documentation Swagger intégrée

### Docker Hub

**Image disponible :** [hammilidi/sentiments_analysis](https://hub.docker.com/r/hammilidi/sentiments_analysis)

```bash
# Utilisation directe depuis Docker Hub
docker pull hammilidi/sentiments_analysis
docker run -p 7860:7860 hammilidi/sentiments_analysis
```

### Structure pour HF Spaces
```
├── Dockerfile              # Point d'entrée Docker
├── app.py                 # Interface Gradio (version Gradio)
├── app/main.py            # API FastAPI (version Docker)
├── static/index.html      # Interface web
├── requirements.txt       # Dépendances
└── README.md             # Documentation
```

### Variables d'environnement
- `PORT=7860` (obligatoire pour HF Spaces)
- `TRANSFORMERS_CACHE=/app/cache` (optimisation)

## ⚙️ Configuration technique

### Modèle utilisé
- **Nom** : `distilbert-base-uncased-finetuned-sst-2-english`
- **Type** : Classification binaire (POSITIVE/NEGATIVE)
- **Avantages** : Léger, rapide, optimisé CPU
- **Performance** : ~77ms par prédiction (CPU)

### Stack technologique
- **API** : FastAPI + Uvicorn
- **Interface** : Gradio
- **ML** : Transformers (Hugging Face)
- **Validation** : Pydantic
- **Conteneurisation** : Docker
- **Tests** : Pytest
- **Frontend** : HTML/CSS/JavaScript

## 🔧 Gestion d'erreurs

L'API gère automatiquement :
- ❌ Texte vide ou contenant seulement des espaces
- ❌ Texte dépassant 1000 caractères
- ❌ Format JSON invalide
- ❌ Champs manquants dans la requête
- ❌ Erreurs du modèle de ML

## 📈 Monitoring et logs

L'API inclut :
- **Logging** des requêtes et erreurs
- **Métriques** de temps de traitement
- **Health check** pour monitoring
- **Validation** complète des entrées

## 🚀 Liens rapides

| Ressource | Lien |
|-----------|------|
| 🎯 **Demo Gradio** | [https://huggingface.co/spaces/Hammilidi/sentiments_analysis](https://huggingface.co/spaces/Hammilidi/sentiments_analysis) |
| 🐳 **Demo Docker** | [https://huggingface.co/spaces/Hammilidi/sentiments_analysis_docker](https://huggingface.co/spaces/Hammilidi/sentiments_analysis_docker) |
| 📦 **GitHub** | [https://github.com/Hammilidi/sentiment_analysis](https://github.com/Hammilidi/sentiment_analysis) |
| 🐋 **Docker Hub** | [hammilidi/sentiments_analysis](https://hub.docker.com/r/hammilidi/sentiments_analysis) |

## 🤝 Contribution

1. Fork le repository : [https://github.com/Hammilidi/sentiment_analysis](https://github.com/Hammilidi/sentiment_analysis)
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues** : [GitHub Issues](https://github.com/Hammilidi/sentiment_analysis/issues)
- **Documentation** : Voir `/docs` pour l'API FastAPI
- **Modèle** : [DistilBERT sur Hugging Face](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)

---

**Développé avec ❤️ par YONLI Fidèle**