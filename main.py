from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
from transformers import pipeline
import logging
import time
from typing import Dict, Any
import uvicorn

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sentiment Analysis API",
    description="API d'analyse de sentiments",
    version="1.0.0"
)

# Modèles Pydantic pour la validation
class TextInput(BaseModel):
    text: str
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Le texte ne peut pas être vide')
        if len(v.strip()) > 1000:
            raise ValueError('Le texte ne peut pas dépasser 1000 caractères')
        return v.strip()

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    text: str
    processing_time_ms: float

# Chargement du modèle au démarrage
logger.info("Chargement du modèle ...")
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english",
        return_all_scores=True
    )
    logger.info("Modèle chargé avec succès")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle: {e}")
    sentiment_analyzer = None

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve la page HTML de test"""
    return FileResponse('static/index.html')

@app.get("/health")
async def health_check():
    """Endpoint de vérification de l'état de l'API"""
    if sentiment_analyzer is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    return {"status": "healthy", "model": "distilbert-base-uncased-finetuned-sst-2-english"}

@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(input_data: TextInput) -> SentimentResponse:
    """
    Analyse le sentiment d'un texte
    
    Args:
        input_data: Objet contenant le texte à analyser
        
    Returns:
        SentimentResponse: Sentiment, confiance et temps de traitement
    """
    if sentiment_analyzer is None:
        logger.error("Tentative d'utilisation du modèle non chargé")
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    start_time = time.time()
    
    try:
        logger.info(f"Analyse du sentiment pour: {input_data.text[:50]}...")
        
        # Analyse du sentiment
        results = sentiment_analyzer(input_data.text)
        
        # Le modèle retourne deux scores (POSITIVE et NEGATIVE)
        # On prend celui avec le score le plus élevé
        positive_score = next(r['score'] for r in results[0] if r['label'] == 'POSITIVE')
        negative_score = next(r['score'] for r in results[0] if r['label'] == 'NEGATIVE')
        
        if positive_score > negative_score:
            sentiment = "POSITIVE"
            confidence = positive_score
        else:
            sentiment = "NEGATIVE" 
            confidence = negative_score
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"Résultat: {sentiment} (confiance: {confidence:.3f})")
        
        return SentimentResponse(
            sentiment=sentiment,
            confidence=round(confidence, 4),
            text=input_data.text,
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'analyse du sentiment")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)