#!/usr/bin/env python3
"""
Script de benchmark pour comparer les performances de différents modèles
de classification de sentiments disponibles sur Hugging Face.
"""

import time
import statistics
from transformers import pipeline
from typing import List, Dict, Tuple
import warnings

# Suppression des warnings pour un affichage plus propre
warnings.filterwarnings("ignore")

class SentimentBenchmark:
    """Classe pour effectuer des benchmarks de modèles de sentiment"""
    
    def __init__(self):
        self.test_sentences = [
            "This product is absolutely amazing! I love it!",
            "Terrible quality, complete waste of money!",
            "It's okay, nothing special but works fine.",
            "Outstanding customer service and fast delivery!",
            "Very disappointed with this purchase.",
            "Good value for money, satisfied overall.",
            "Awful experience, would not recommend.",
            "Excellent quality and great features!",
            "Not worth the price, poor performance.",
            "Perfect! Exactly what I was looking for!"
        ]
        
        # Labels attendus (pour évaluation de la justesse)
        self.expected_labels = [
            "POSITIVE", "NEGATIVE", "NEUTRAL", "POSITIVE", "NEGATIVE",
            "POSITIVE", "NEGATIVE", "POSITIVE", "NEGATIVE", "POSITIVE"
        ]
        
    def load_model(self, model_name: str) -> pipeline:
        """Charge un modèle de classification de sentiments"""
        try:
            print(f"Chargement du modèle: {model_name}")
            start_time = time.time()
            
            if "cardiffnlp" in model_name:
                # Modèles Cardiff ont une structure différente
                sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=model_name,
                    return_all_scores=True
                )
            else:
                sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=model_name,
                    return_all_scores=True
                )
                
            load_time = time.time() - start_time
            print(f"Modèle chargé en {load_time:.2f}s")
            return sentiment_pipeline
            
        except Exception as e:
            print(f"Erreur lors du chargement de {model_name}: {e}")
            return None
    
    def benchmark_model(self, model_pipeline: pipeline, model_name: str) -> Dict:
        """Effectue le benchmark d'un modèle"""
        if model_pipeline is None:
            return None
            
        print(f"\n=== Benchmark de {model_name} ===")
        
        latencies = []
        predictions = []
        correct_predictions = 0
        
        for i, sentence in enumerate(self.test_sentences):
            try:
                # Mesure du temps de traitement
                start_time = time.time()
                results = model_pipeline(sentence)
                latency = (time.time() - start_time) * 1000  # en ms
                latencies.append(latency)
                
                # Extraction du sentiment dominant
                if isinstance(results[0], list):
                    # Format avec tous les scores
                    best_result = max(results[0], key=lambda x: x['score'])
                    sentiment = best_result['label']
                    confidence = best_result['score']
                else:
                    # Format simple
                    sentiment = results[0]['label']
                    confidence = results[0]['score']
                
                # Normalisation des labels
                if sentiment in ['LABEL_1', '1', 'POS']:
                    sentiment = 'POSITIVE'
                elif sentiment in ['LABEL_0', '0', 'NEG']:
                    sentiment = 'NEGATIVE'
                elif sentiment in ['LABEL_2', '2', 'NEU']:
                    sentiment = 'NEUTRAL'
                    
                predictions.append(sentiment)
                
                # Vérification de la justesse (approximative)
                expected = self.expected_labels[i]
                if expected == 'NEUTRAL' or sentiment == expected:
                    correct_predictions += 1
                    
                print(f"  {i+1:2d}. '{sentence[:50]}...' → {sentiment} ({confidence:.3f}) [{latency:.1f}ms]")
                
            except Exception as e:
                print(f"  Erreur sur phrase {i+1}: {e}")
                continue
        
        # Calcul des statistiques
        if latencies:
            avg_latency = statistics.mean(latencies)
            median_latency = statistics.median(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            accuracy = correct_predictions / len(self.test_sentences)
            
            return {
                'model_name': model_name,
                'avg_latency_ms': avg_latency,
                'median_latency_ms': median_latency,
                'min_latency_ms': min_latency,
                'max_latency_ms': max_latency,
                'accuracy': accuracy,
                'total_tests': len(self.test_sentences),
                'successful_predictions': len(latencies)
            }
        else:
            return None
    
    def run_comparative_benchmark(self):
        """Lance un benchmark comparatif entre plusieurs modèles"""
        
        models_to_test = [
            "distilbert-base-uncased-finetuned-sst-2-english",  # Modèle principal
            "cardiffnlp/twitter-roberta-base-sentiment-latest",  # Alternative populaire
        ]
        
        print("🚀 Démarrage du benchmark comparatif")
        print("=" * 60)
        
        results = []
        
        for model_name in models_to_test:
            model_pipeline = self.load_model(model_name)
            result = self.benchmark_model(model_pipeline, model_name)
            if result:
                results.append(result)
                
        # Affichage du tableau comparatif
        if results:
            print("\n" + "=" * 80)
            print("📊 RÉSULTATS COMPARATIFS")
            print("=" * 80)
            
            # En-tête du tableau
            print(f"{'Modèle':<50} {'Latence Moy.':<12} {'Précision':<10} {'Min/Max':<15}")
            print("-" * 80)
            
            # Données des modèles
            for result in results:
                model_short = result['model_name'].split('/')[-1][:45]
                avg_lat = f"{result['avg_latency_ms']:.1f}ms"
                accuracy = f"{result['accuracy']*100:.1f}%"
                min_max = f"{result['min_latency_ms']:.0f}/{result['max_latency_ms']:.0f}ms"
                
                print(f"{model_short:<50} {avg_lat:<12} {accuracy:<10} {min_max:<15}")
            
            # Recommandation
            print("\n💡 RECOMMANDATION:")
            best_overall = min(results, key=lambda x: x['avg_latency_ms'] * (2 - x['accuracy']))
            print(f"   Meilleur équilibre performance/précision: {best_overall['model_name']}")
            
        return results

def main():
    """Fonction principale"""
    benchmark = SentimentBenchmark()
    results = benchmark.run_comparative_benchmark()
    
    # Sauvegarde des résultats
    if results:
        print(f"\n✅ Benchmark terminé avec succès!")
        print(f"   {len(results)} modèle(s) testé(s)")
        print(f"   {len(benchmark.test_sentences)} phrases de test")

if __name__ == "__main__":
    main()