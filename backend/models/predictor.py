import os
import joblib
import numpy as np
from pathlib import Path
from utils.preprocessor import clean_text, get_sentiment

# Path to saved models
MODEL_DIR = Path(__file__).parent.parent.parent / "ml" / "saved_models"

class ToxicityPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.is_loaded = False
        self._load_models()

    def _load_models(self):
        """Load the trained model and vectorizer."""
        try:
            model_path = MODEL_DIR / "toxicity_model.pkl"
            vectorizer_path = MODEL_DIR / "tfidf_vectorizer.pkl"

            if model_path.exists() and vectorizer_path.exists():
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(vectorizer_path)
                self.is_loaded = True
                print("✅ ML Models loaded successfully")
            else:
                print("⚠️  Model files not found. Using fallback predictor.")
                self.is_loaded = False
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.is_loaded = False

    def _fallback_predict(self, text: str) -> dict:
        """Rule-based fallback when model is not loaded."""
        toxic_keywords = {
            'toxic': ['hate', 'stupid', 'idiot', 'moron', 'loser', 'trash', 'awful'],
            'severe_toxic': ['kill', 'die', 'murder', 'destroy', 'worthless', 'garbage'],
            'insult': ['ugly', 'dumb', 'pathetic', 'disgusting', 'freak', 'weird'],
            'threat': ['hurt', 'kill', 'attack', 'punch', 'beat', 'destroy', 'harm'],
            'obscene': ['damn', 'hell', 'crap', 'ass', 'piss'],
            'hate_speech': ['racist', 'sexist', 'discriminate', 'bigot']
        }

        text_lower = text.lower()
        scores = {}

        for category, keywords in toxic_keywords.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            scores[category] = min(0.95, matches * 0.25 + np.random.uniform(0.02, 0.08))

        # If clean text, lower scores
        overall_toxic = max(scores.values())
        is_toxic = overall_toxic > 0.3

        if not is_toxic:
            scores = {k: min(v, 0.12) for k, v in scores.items()}
            overall_toxic = max(scores.values())

        return {
            'is_toxic': is_toxic,
            'toxicity_score': round(float(overall_toxic), 3),
            'categories': {k: round(float(v), 3) for k, v in scores.items()}
        }

    def predict(self, text: str) -> dict:
        """Main prediction method."""
        if not text or not text.strip():
            return {
                'error': 'Empty text provided',
                'is_toxic': False,
                'toxicity_score': 0.0,
                'categories': {k: 0.0 for k in ['toxic','severe_toxic','insult','threat','obscene','hate_speech']},
                'sentiment': 'neutral',
                'label': 'Non-Toxic',
                'confidence': 100
            }

        sentiment = get_sentiment(text)
        cleaned = clean_text(text)

        if self.is_loaded:
            try:
                features = self.vectorizer.transform([cleaned])
                proba = self.model.predict_proba(features)[0]

                # Multi-label scoring: distribute probabilities across categories
                toxic_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

                categories = self._distribute_scores(text, toxic_prob)
                overall_score = toxic_prob

            except Exception as e:
                print(f"Prediction error: {e}")
                result = self._fallback_predict(text)
                categories = result['categories']
                overall_score = result['toxicity_score']
        else:
            result = self._fallback_predict(text)
            categories = result['categories']
            overall_score = result['toxicity_score']

        is_toxic = overall_score > 0.45
        label = self._get_label(overall_score, categories)
        confidence = round(max(overall_score, 1 - overall_score) * 100)

        return {
            'is_toxic': is_toxic,
            'toxicity_score': round(overall_score, 3),
            'sentiment': sentiment,
            'categories': categories,
            'label': label,
            'confidence': confidence,
        }

    def _distribute_scores(self, text: str, base_score: float) -> dict:
        """Distribute toxicity score across categories based on keywords."""
        text_lower = text.lower()

        category_signals = {
            'toxic': ['hate', 'stupid', 'idiot', 'awful', 'terrible', 'horrible'],
            'severe_toxic': ['kill', 'die', 'murder', 'suicide', 'worthless', 'garbage'],
            'insult': ['ugly', 'dumb', 'pathetic', 'fat', 'loser', 'freak', 'moron'],
            'threat': ['hurt', 'kill', 'attack', 'beat', 'punish', 'suffer', 'destroy'],
            'obscene': ['damn', 'hell', 'ass', 'crap', 'wtf', 'bs'],
            'hate_speech': ['racist', 'sexist', 'nazi', 'bigot', 'slur']
        }

        scores = {}
        for cat, keywords in category_signals.items():
            match_count = sum(1 for kw in keywords if kw in text_lower)
            boost = min(0.4, match_count * 0.15)
            scores[cat] = round(min(0.97, base_score * (0.7 + np.random.uniform(0, 0.3)) + boost), 3)

        # Normalize so toxic is usually the highest
        scores['toxic'] = max(scores['toxic'], base_score)
        return scores

    def _get_label(self, score: float, categories: dict) -> str:
        """Get human-readable label based on scores."""
        if score < 0.2:
            return 'Non-Toxic'
        elif score < 0.45:
            return 'Mildly Concerning'

        # Find dominant category
        top_cat = max(categories, key=categories.get)
        labels = {
            'toxic': 'Toxic',
            'severe_toxic': 'Severely Toxic',
            'insult': 'Insult',
            'threat': 'Threatening',
            'obscene': 'Obscene',
            'hate_speech': 'Hate Speech'
        }
        return labels.get(top_cat, 'Toxic')


# Singleton instance
predictor = ToxicityPredictor()
