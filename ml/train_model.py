"""
Model Training Script
======================
Trains a multi-label toxicity classification model.

Pipeline:
  Raw text → TF-IDF Vectorizer → Logistic Regression (OneVsRest)

Run: python train_model.py
"""

import os
import pickle
import warnings
import numpy as np
import joblib

warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    f1_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

PROCESSED_DATA_PATH = "datasets/processed_data.pkl"
MODEL_DIR = "saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

# ──────────────────────────────────────────────
# Load Preprocessed Data
# ──────────────────────────────────────────────
def load_data():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print("❌ Processed data not found. Run preprocess_data.py first.")
        raise FileNotFoundError(PROCESSED_DATA_PATH)

    with open(PROCESSED_DATA_PATH, "rb") as f:
        data = pickle.load(f)

    X = data["X"]
    y = data["y"]
    label_columns = data["label_columns"]

    print(f"✅ Loaded {len(X)} samples with {len(label_columns)} labels")
    print(f"   Labels: {label_columns}")
    return X, y, label_columns


# ──────────────────────────────────────────────
# Build & Train Pipeline
# ──────────────────────────────────────────────
def train(X, y, label_columns):
    print("\n🔄 Splitting dataset (80/20 train/test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y[:, 0]
    )
    print(f"   Train: {len(X_train)} | Test: {len(X_test)}")

    # ── TF-IDF Vectorizer ──────────────────────
    print("\n🔄 Building TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),       # unigrams + bigrams
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,        # apply log normalization
        strip_accents="unicode",
        analyzer="word",
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")

    # ── Logistic Regression (OneVsRest multi-label) ──
    print("\n🔄 Training Logistic Regression (OneVsRest)...")
    base_clf = LogisticRegression(
        C=1.0,
        solver="lbfgs",
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )
    clf = OneVsRestClassifier(base_clf, n_jobs=-1)
    clf.fit(X_train_vec, y_train)
    print("   Training complete ✅")

    # ── Evaluation ────────────────────────────
    print("\n📊 Evaluating on test set...")
    y_pred = clf.predict(X_test_vec)
    y_prob = clf.predict_proba(X_test_vec)

    # Per-label metrics
    for i, label in enumerate(label_columns):
        acc = accuracy_score(y_test[:, i], y_pred[:, i])
        f1  = f1_score(y_test[:, i], y_pred[:, i], zero_division=0)
        print(f"   {label:15s}  acc={acc:.3f}  f1={f1:.3f}")

    # Overall
    f1_micro = f1_score(y_test, y_pred, average="micro", zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    print(f"\n   Micro F1: {f1_micro:.4f}")
    print(f"   Macro F1: {f1_macro:.4f}")

    try:
        auc = roc_auc_score(y_test, y_prob, average="macro")
        print(f"   ROC AUC:  {auc:.4f}")
    except Exception:
        pass

    # ── Save Artifacts ────────────────────────
    vectorizer_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
    model_path      = os.path.join(MODEL_DIR, "toxicity_model.pkl")
    meta_path       = os.path.join(MODEL_DIR, "model_meta.pkl")

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(clf,        model_path)
    joblib.dump({"label_columns": label_columns, "f1_micro": f1_micro}, meta_path)

    print(f"\n✅ Model artifacts saved:")
    print(f"   {vectorizer_path}")
    print(f"   {model_path}")
    print(f"   {meta_path}")

    return clf, vectorizer, label_columns


# ──────────────────────────────────────────────
# Quick Inference Test
# ──────────────────────────────────────────────
def test_inference(clf, vectorizer, label_columns):
    print("\n🧪 Quick inference test...")
    test_cases = [
        "You are such an idiot, I hate you so much",
        "I disagree with your point but I respect your opinion",
        "I will find you and hurt you if you do that again",
        "Have a wonderful day, hope things go well for you!",
        "You ugly disgusting piece of trash nobody likes you",
    ]

    for text in test_cases:
        vec  = vectorizer.transform([text])
        prob = clf.predict_proba(vec)[0]
        toxic_score = prob[label_columns.index("toxic")] if "toxic" in label_columns else prob[0]
        label = "🔴 TOXIC" if toxic_score > 0.5 else "🟢 CLEAN"
        print(f"   {label} ({toxic_score:.2f}) | {text[:60]}")


if __name__ == "__main__":
    print("=" * 60)
    print("  Toxicity Model Training Script")
    print("=" * 60)

    X, y, label_columns = load_data()
    clf, vectorizer, label_columns = train(X, y, label_columns)
    test_inference(clf, vectorizer, label_columns)

    print("\n🎉 Training complete! Start the backend: python app.py")
