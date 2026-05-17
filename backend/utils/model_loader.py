"""
Loads the saved TF-IDF vectorizer and per-category classifiers.
Falls back to a rule-based heuristic when model files are absent.
"""
import os
import re
import joblib
import numpy as np

MODEL_PATH = os.getenv("MODEL_PATH", "../ml/saved_models/")

_vectorizer = None
_models = {}

CATEGORIES = ["toxic", "severe_toxic", "insult", "threat", "obscene", "hate_speech"]

# ── Toxic keywords for fallback heuristic ────────────────────────────────────
TOXIC_KEYWORDS = {
    "toxic":        ["idiot", "stupid", "dumb", "moron", "loser", "hate", "suck"],
    "severe_toxic": ["kill yourself", "die", "worst person", "piece of"],
    "insult":       ["ugly", "fat", "useless", "pathetic", "failure"],
    "threat":       ["i will kill", "i will hurt", "watch your back", "you will pay"],
    "obscene":      ["fuck", "shit", "ass", "bitch", "crap"],
    "hate_speech":  ["slur", "racist", "bigot"],
}


def _load_models():
    global _vectorizer, _models
    vec_path = os.path.join(MODEL_PATH, "tfidf_vectorizer.pkl")
    if not os.path.exists(vec_path):
        return False
    _vectorizer = joblib.load(vec_path)
    for cat in CATEGORIES:
        path = os.path.join(MODEL_PATH, f"model_{cat}.pkl")
        if os.path.exists(path):
            _models[cat] = joblib.load(path)
    return True


def _heuristic_predict(text: str) -> dict:
    """Simple keyword-based fallback used before the real model is trained."""
    text_lower = text.lower()
    scores = {}
    for cat, keywords in TOXIC_KEYWORDS.items():
        hit = sum(1 for kw in keywords if kw in text_lower)
        scores[cat] = min(0.15 + hit * 0.20, 0.99) if hit else round(np.random.uniform(0.01, 0.08), 3)

    toxicity_score = max(scores.values())
    return scores, toxicity_score


def predict(text: str, preprocessed: str) -> dict:
    """
    Returns:
        categories: dict of {label: probability}
        toxicity_score: float — overall worst-case score
        sentiment: str
    """
    use_ml = _load_models() and bool(_models)

    if use_ml:
        X = _vectorizer.transform([preprocessed])
        scores = {}
        for cat in CATEGORIES:
            if cat in _models:
                prob = _models[cat].predict_proba(X)[0][1]
                scores[cat] = round(float(prob), 4)
            else:
                scores[cat] = 0.0
        toxicity_score = max(scores.values())
    else:
        scores, toxicity_score = _heuristic_predict(text)

    # Simple sentiment heuristic
    positive_words = ["love", "great", "awesome", "good", "wonderful", "happy", "thanks"]
    negative_words = ["hate", "bad", "terrible", "awful", "horrible", "stupid"]
    t = text.lower()
    pos = sum(1 for w in positive_words if w in t)
    neg = sum(1 for w in negative_words if w in t)
    if pos > neg:
        sentiment = "positive"
    elif neg > pos or toxicity_score > 0.4:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "categories": {k: round(v, 4) for k, v in scores.items()},
        "toxicity_score": round(float(toxicity_score), 4),
        "sentiment": sentiment,
        "model_used": "ml_model" if use_ml else "heuristic_fallback",
    }
