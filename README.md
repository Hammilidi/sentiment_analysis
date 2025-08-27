# 🎯 Sentiment Analysis API

API d'analyse de sentiments utilisant **DistilBERT** pour classifier automatiquement les textes en sentiments positifs ou négatifs avec un score de confiance.

## 🚀 Démo en ligne

**🌐 Application déployée :** [https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-api](https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-api)

## ✨ Fonctionnalités

- **Analyse de sentiment** : Classification POSITIVE/NEGATIVE avec score de confiance
- **API REST** complète avec validation des données
- **Interface web** intuitive pour tester l'API
- **Documentation automatique** avec Swagger UI
- **Conteneurisé** avec Docker
- **Déployé** sur Hugging Face Spaces
- **Tests unitaires** et benchmark de performance

## 🏗️ Architecture

```
sentiment-analysis-api/
├── app/
│   └── main.py              # API FastAPI principale
├── static/
│   └── index.html           # Interface web de test
├── tests/
│   └── test_api.py          # Tests unitaires
├── Dockerfile               # Configuration Docker
├── requirements.txt         # Dépendances Python
├── benchmark.py            # Script de benchmark
└── README.md               # Documentation
```

## 🛠️ Installation et utilisation

### Option 1: Lancement local avec Docker (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/YOUR_USERNAME/sentiment-analysis-api.git
cd sentiment-analysis-api

# Construire l'image Docker
docker build -t sentiment-api .

# Lancer le container
docker run -p 7860:7860 sentiment-api
```

### Option 2: Lancement avec Uvicorn

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
cd app
uvicorn main:app --host 0.0.0.0 --port 7860 --reload
```

### Accès à l'application

- **Interface web** : http://localhost:7860
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

**Réponse :**
```json
{
  "sentiment": "POSITIVE",
  "confidence": 0.9998,
  "text": "This product is amazing!",
  "processing_time_ms": 45.2
}
```

### Autres endpoints

- `GET /` - Interface web de test
- `GET /health` - Vérification de l'état de l'API  
- `GET /docs` - Documentation Swagger interactive

## 🧪 Tests et validation

### Lancer les tests unitaires

```bash
# Installation de pytest
pip install pytest

# Exécution des tests
python -m pytest test_api.py -v
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
- **Performance** : temps de réponse < 5 secondes

### Benchmark comparatif

| Modèle | Latence Moyenne | Précision | Min/Max |
|--------|----------------|-----------|---------|
| **distilbert-base-uncased-finetuned-sst-2-english** | **52.3ms** | **90%** | 31/78ms |
| cardiffnlp/twitter-roberta-base-sentiment-latest | 89.7ms | 85% | 67/134ms |

**🏆 Recommandation :** DistilBERT offre le meilleur équilibre performance/précision.

### Cas de test types

| Texte | Sentiment attendu | Résultat |
|-------|------------------|----------|
| "This product is absolutely amazing!" | POSITIVE ✅ | POSITIVE (99.8%) |
| "Terrible quality, waste of money!" | NEGATIVE ✅ | NEGATIVE (99.2%) |
| "It works fine, nothing special." | NEUTRAL ➡️ | POSITIVE (65.4%) |

## 🐳 Déploiement sur Hugging Face Spaces

### Configuration requise

1. **Créer un Space** sur [Hugging Face](https://huggingface.co/spaces)
2. **Sélectionner** "Docker" comme SDK
3. **Uploader** tous les fichiers du projet

### Structure pour HF Spaces
```
├── Dockerfile              # Point d'entrée Docker
├── app/main.py            # API FastAPI
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
- **Performance** : ~50ms par prédiction

### Stack technologique
- **API** : FastAPI + Uvicorn
- **ML** : Transformers (Hugging Face)
- **Validation** : Pydantic
- **Conteneurisation** : Docker
- **Tests** : Pytest
- **Interface** : HTML/CSS/JavaScript

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

## 🤝 Contribution

1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues** : [GitHub Issues](https://github.com/YOUR_USERNAME/sentiment-analysis-api/issues)
- **Documentation** : Voir `/docs` quand l'API est lancée
- **Modèle** : [DistilBERT sur Hugging Face](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)

---

**Développé avec ❤️ by YONLI Fidele**