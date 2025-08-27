import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ajout du répertoire app au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from main import app

client = TestClient(app)

class TestSentimentAPI:
    """Tests unitaires pour l'API d'analyse de sentiments"""
    
    def test_health_check(self):
        """Test de l'endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model" in data
        
    def test_predict_positive_sentiment(self):
        """Test d'analyse d'un sentiment positif"""
        response = client.post(
            "/predict",
            json={"text": "This product is amazing! I love it so much!"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Vérification de la structure de la réponse
        assert "sentiment" in data
        assert "confidence" in data
        assert "text" in data
        assert "processing_time_ms" in data
        
        # Vérification du sentiment (devrait être positif)
        assert data["sentiment"] == "POSITIVE"
        assert 0 <= data["confidence"] <= 1
        assert data["processing_time_ms"] > 0
        
    def test_predict_negative_sentiment(self):
        """Test d'analyse d'un sentiment négatif"""
        response = client.post(
            "/predict",
            json={"text": "This is terrible! I hate it completely!"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Vérification du sentiment (devrait être négatif)
        assert data["sentiment"] == "NEGATIVE"
        assert 0 <= data["confidence"] <= 1
        assert data["processing_time_ms"] > 0
        
    def test_predict_empty_text(self):
        """Test avec un texte vide (devrait retourner une erreur)"""
        response = client.post(
            "/predict",
            json={"text": ""}
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        
    def test_predict_whitespace_only(self):
        """Test avec seulement des espaces (devrait retourner une erreur)"""
        response = client.post(
            "/predict",
            json={"text": "   "}
        )
        assert response.status_code == 422
        
    def test_predict_long_text(self):
        """Test avec un texte trop long (devrait retourner une erreur)"""
        long_text = "This is a very long text. " * 50  # Plus de 1000 caractères
        response = client.post(
            "/predict",
            json={"text": long_text}
        )
        assert response.status_code == 422
        
    def test_predict_invalid_json(self):
        """Test avec un JSON invalide"""
        response = client.post(
            "/predict",
            json={"wrong_field": "some text"}
        )
        assert response.status_code == 422
        
    def test_predict_normal_text(self):
        """Test avec un texte neutre/normal"""
        response = client.post(
            "/predict",
            json={"text": "The weather is okay today."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] in ["POSITIVE", "NEGATIVE"]
        assert 0 <= data["confidence"] <= 1
        
    def test_root_endpoint(self):
        """Test de l'endpoint racine (devrait servir le fichier HTML)"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
    def test_docs_endpoint(self):
        """Test de l'endpoint de documentation Swagger"""
        response = client.get("/docs")
        assert response.status_code == 200
        
    def test_openapi_endpoint(self):
        """Test de l'endpoint OpenAPI"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "info" in data
        assert data["info"]["title"] == "Sentiment Analysis API"

# Tests de benchmark (bonus)
class TestBenchmark:
    """Tests de performance et benchmark"""
    
    def test_response_time(self):
        """Test du temps de réponse"""
        import time
        
        start_time = time.time()
        response = client.post(
            "/predict",
            json={"text": "This is a test for response time measurement"}
        )
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000  # en ms
        
        # Le temps de réponse devrait être raisonnable (< 5 secondes)
        assert response_time < 5000
        
        # Vérification que le temps interne correspond approximativement
        data = response.json()
        internal_time = data["processing_time_ms"]
        
        # Le temps interne devrait être inférieur au temps total
        assert internal_time < response_time
        
    def test_multiple_predictions_consistency(self):
        """Test de cohérence sur plusieurs prédictions"""
        test_text = "This product is absolutely fantastic!"
        
        results = []
        for _ in range(3):
            response = client.post("/predict", json={"text": test_text})
            assert response.status_code == 200
            results.append(response.json())
        
        # Tous les résultats devraient avoir le même sentiment
        sentiments = [r["sentiment"] for r in results]
        assert len(set(sentiments)) == 1  # Tous identiques
        
        # Les scores de confiance devraient être identiques ou très proches
        confidences = [r["confidence"] for r in results]
        assert max(confidences) - min(confidences) < 0.001

if __name__ == "__main__":
    # Exécution des tests
    pytest.main([__file__, "-v"])